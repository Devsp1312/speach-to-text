"""
Inference Module
================

This module handles making predictions on new text:
1. Single prediction on a short text
2. Long transcript handling (chunking + averaging)
3. Confidence scoring with threshold filtering
4. User profile generation from predictions

Key Features:
- Top-3 predictions with probabilities
- "Unknown / Low Signal" handling (confidence < 0.45)
- Long transcript chunking (100-200 words per chunk)
- Per-chunk predictions with averaging
- Profile aggregation from multiple chunks
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import re


class InterestPredictor:
    """
    Make predictions using trained interest classifier.
    """
    
    def __init__(self, classifier):
        """
        Initialize predictor with trained classifier.
        
        Args:
            classifier: Trained InterestClassifier instance
        """
        self.classifier = classifier
        self.confidence_threshold = 0.45
    
    
    def predict_single(self, text: str, top_n: int = 3) -> Dict:
        """
        Predict interests from a single text.
        
        Args:
            text: Input text
            top_n: Number of top predictions to return
        
        Returns:
            Dictionary with predictions and confidence scores
        """
        
        # Vectorize text
        text_vector = self.classifier.vectorizer.transform([text.lower()])
        
        # Get predictions
        pred_idx = self.classifier.model.predict(text_vector)[0]
        pred_label = self.classifier.label_info['idx_to_label'][pred_idx]
        
        # Get probabilities for all classes
        probabilities = self.classifier.model.predict_proba(text_vector)[0]
        
        # Get top N predictions
        top_indices = np.argsort(probabilities)[-top_n:][::-1]
        
        predictions = []
        for idx in top_indices:
            label = self.classifier.label_info['idx_to_label'][idx]
            confidence = float(probabilities[idx])
            
            # Check if confidence meets threshold
            if confidence < self.confidence_threshold:
                confidence_level = "low"
            else:
                confidence_level = "high"
            
            predictions.append({
                'interest': label,
                'confidence': confidence,
                'confidence_level': confidence_level,
            })
        
        # Check if top prediction is above threshold
        if predictions[0]['confidence'] < self.confidence_threshold:
            return {
                'primary': "Unknown / Low Signal",
                'confidence': float(predictions[0]['confidence']),
                'all_predictions': predictions,
                'interpretation': "Confidence too low to determine interest profile."
            }
        
        return {
            'primary': predictions[0]['interest'],
            'confidence': predictions[0]['confidence'],
            'all_predictions': predictions,
            'interpretation': f"High confidence in {predictions[0]['interest']} interest."
        }
    
    
    def split_into_chunks(self, text: str, words_per_chunk: int = 150) -> List[str]:
        """
        Split long transcript into overlapping chunks.
        
        Args:
            text: Long transcript text
            words_per_chunk: Target words per chunk (100-200 recommended)
        
        Returns:
            List of text chunks
        """
        
        # Split into words
        words = text.split()
        
        # Create overlapping chunks
        chunks = []
        stride = int(words_per_chunk * 0.75)  # 75% overlap
        
        for i in range(0, len(words), stride):
            chunk = ' '.join(words[i:i + words_per_chunk])
            if len(chunk.split()) >= 20:  # Only include chunks with ≥20 words
                chunks.append(chunk)
        
        # Ensure we don't miss the end
        if words[-(words_per_chunk//2):]:
            final_chunk = ' '.join(words[-(words_per_chunk//2):])
            if final_chunk not in chunks:
                chunks.append(final_chunk)
        
        return chunks
    
    
    def predict_long_transcript(self, transcript: str, words_per_chunk: int = 150) -> Dict:
        """
        Predict interests from a long transcript (e.g., 5-minute conversation).
        
        Process:
        1. Split transcript into chunks (~150 words each with 75% overlap)
        2. Predict interests for each chunk
        3. Average probabilities across all chunks
        4. Return aggregated profile
        
        Args:
            transcript: Long conversation transcript
            words_per_chunk: Words per chunk (100-200 recommended)
        
        Returns:
            Dictionary with aggregated predictions
        """
        
        print(f"\n📝 Processing long transcript ({len(transcript.split())} words)...")
        
        # Split into chunks
        chunks = self.split_into_chunks(transcript, words_per_chunk)
        print(f"  ✓ Split into {len(chunks)} chunks (~{words_per_chunk} words each)")
        
        # Predict for each chunk
        chunk_predictions = []
        for i, chunk in enumerate(chunks):
            pred = self.predict_single(chunk)
            chunk_predictions.append(pred)
            print(f"  Chunk {i+1}: {pred['primary']} ({pred['confidence']:.2%})")
        
        # Average probabilities across chunks
        all_probs = {}
        for label_idx, label in self.classifier.label_info['idx_to_label'].items():
            probs = []
            for chunk in chunks:
                chunk_vector = self.classifier.vectorizer.transform([chunk.lower()])
                chunk_probs = self.classifier.model.predict_proba(chunk_vector)[0]
                probs.append(chunk_probs[label_idx])
            all_probs[label] = np.mean(probs)
        
        # Sort by averaged probability
        sorted_interests = sorted(all_probs.items(), key=lambda x: x[1], reverse=True)
        
        # Build aggregated profile
        profile = {
            'top_interest': sorted_interests[0][0],
            'top_confidence': float(sorted_interests[0][1]),
            'all_interests': [
                {
                    'interest': label,
                    'confidence': float(conf)
                }
                for label, conf in sorted_interests
            ],
            'chunks_analyzed': len(chunks),
            'total_words': len(transcript.split()),
        }
        
        # Check if top confidence meets threshold
        if profile['top_confidence'] < self.confidence_threshold:
            profile['primary'] = "Unknown / Low Signal"
            profile['interpretation'] = "Mixed interests or unclear transcript - confidence too low."
        else:
            profile['primary'] = profile['top_interest']
            profile['interpretation'] = f"Dominant interest: {profile['top_interest']} ({profile['top_confidence']:.1%})"
        
        return profile
    
    
    def get_user_profile(self, interests_dict: Dict[str, float]) -> Dict[str, str]:
        """
        Generate a readable user profile from interest scores.
        
        This function creates a human-readable summary based on interest distribution.
        
        Args:
            interests_dict: Dictionary mapping interests to confidence scores
        
        Returns:
            Dictionary with profile descriptions
        """
        
        # Sort by confidence
        sorted_interests = sorted(interests_dict.items(), key=lambda x: x[1], reverse=True)
        top_interests = [interest for interest, _ in sorted_interests[:3]]
        
        # Generate profile description
        if len(top_interests) == 0:
            profile_desc = "No clear interests detected."
        elif len(top_interests) == 1:
            profile_desc = f"Focused on {top_interests[0]}."
        else:
            desc = ", ".join(top_interests[:-1])
            profile_desc = f"Interested in {desc}, and {top_interests[-1]}."
        
        return {
            'profile': profile_desc,
            'top_interests': top_interests,
        }


def batch_predict(predictor: InterestPredictor, texts: List[str]) -> List[Dict]:
    """
    Make predictions on multiple texts.
    
    Args:
        predictor: InterestPredictor instance
        texts: List of text samples
    
    Returns:
        List of prediction dictionaries
    """
    
    results = []
    for text in texts:
        result = predictor.predict_single(text)
        results.append(result)
    
    return results


def create_prediction_dataframe(predictor: InterestPredictor, texts: List[str]) -> pd.DataFrame:
    """
    Create a DataFrame of predictions for batch analysis.
    
    Args:
        predictor: InterestPredictor instance
        texts: List of text samples
    
    Returns:
        DataFrame with predictions
    """
    
    predictions = batch_predict(predictor, texts)
    
    data = []
    for text, pred in zip(texts, predictions):
        data.append({
            'text': text[:100] + '...' if len(text) > 100 else text,
            'primary_interest': pred['primary'],
            'confidence': pred['confidence'],
            'top_3': ', '.join([p['interest'] for p in pred['all_predictions'][:3]]),
        })
    
    return pd.DataFrame(data)


# Example usage
if __name__ == "__main__":
    from ml_classifier import InterestClassifier
    
    # Load pre-trained model (assuming it exists)
    try:
        classifier = InterestClassifier.load_model("interest_classifier")
        predictor = InterestPredictor(classifier)
        
        # Test single prediction
        test_text = "I love programming, building websites, and learning about machine learning."
        print("Single Prediction:")
        print(predictor.predict_single(test_text))
        
        # Test long transcript
        long_text = """
        So I've been really into gaming lately, particularly competitive esports. 
        I play a lot of strategy games and I'm always watching tournaments online.
        But I also enjoy social activities - going out with friends, meeting new people at gaming events.
        I think what draws me most is the combination of strategic thinking and community aspect.
        My friends joke that I'm always talking about games or organizing gaming meetups.
        """
        print("\n\nLong Transcript Prediction:")
        print(predictor.predict_long_transcript(long_text))
        
    except FileNotFoundError:
        print("Model not found. Please train model first using ml_classifier.py")
