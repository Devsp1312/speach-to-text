"""
Model Training Module
====================

This module handles:
1. TF-IDF vectorization with optimized parameters
2. Logistic Regression classifier training
3. Model evaluation (accuracy, precision, recall, F1)
4. Confusion matrix visualization
5. Feature importance analysis

Model Architecture:
- Vectorizer: TfidfVectorizer
  - lowercase: True (normalize text)
  - ngram_range: (1, 2) (unigrams + bigrams for context)
  - min_df: 2 (ignore words in <2 documents)
  - max_df: 0.9 (ignore words in >90% of documents)
  - max_features: ~50,000 (limit vocabulary size)
  
- Classifier: LogisticRegression
  - max_iter: 1000+ (ensure convergence)
  - class_weight: 'balanced' (handle imbalanced classes)
  - random_state: 42 (reproducibility)

Why these parameters?
- TF-IDF: Captures topic-specific vocabulary effectively
- Balanced weights: Prevents model from biasing toward majority class
- Logistic Regression: Fast, interpretable, provides confidence scores
"""

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report
)
import pickle
from pathlib import Path
from typing import Tuple, Dict, Any
import matplotlib.pyplot as plt
import seaborn as sns


class InterestClassifier:
    """
    TF-IDF + Logistic Regression classifier for interest prediction.
    
    Attributes:
        vectorizer: TfidfVectorizer instance
        model: LogisticRegression instance
        label_info: Dictionary with label encoding/decoding
    """
    
    def __init__(self, label_info: Dict):
        """
        Initialize the classifier.
        
        Args:
            label_info: Dictionary from preprocessing module with label metadata
        """
        self.label_info = label_info
        
        # Initialize TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),  # Unigrams and bigrams
            min_df=2,
            max_df=0.9,
            max_features=50000,
            stop_words='english'
        )
        
        # Initialize classifier
        self.model = LogisticRegression(
            max_iter=1000,
            class_weight='balanced',
            random_state=42,
            n_jobs=-1  # Use all CPU cores
        )
        
        self.is_fitted = False
    
    
    def train(self, X_train: pd.Series, y_train: pd.Series) -> Dict[str, float]:
        """
        Train the model on labeled data.
        
        Args:
            X_train: Training texts
            y_train: Training labels
        
        Returns:
            Dictionary with training metrics
        """
        
        print("🔄 Training model...")
        
        # Encode labels to indices
        y_train_encoded = y_train.map(self.label_info['label_to_idx'])
        
        # Vectorize training text
        print("  → Vectorizing training texts...")
        X_train_vectors = self.vectorizer.fit_transform(X_train)
        print(f"    ✓ Created {X_train_vectors.shape[1]} features")
        
        # Train classifier
        print("  → Fitting Logistic Regression...")
        self.model.fit(X_train_vectors, y_train_encoded)
        self.is_fitted = True
        
        # Calculate training accuracy
        train_pred = self.model.predict(X_train_vectors)
        train_accuracy = accuracy_score(y_train_encoded, train_pred)
        
        print(f"✓ Training complete! (Accuracy: {train_accuracy:.3f})")
        
        return {'accuracy': train_accuracy}
    
    
    def evaluate(self, X_test: pd.Series, y_test: pd.Series) -> Dict[str, Any]:
        """
        Evaluate model on test data.
        
        Args:
            X_test: Test texts
            y_test: Test labels
        
        Returns:
            Dictionary with evaluation metrics
        """
        
        if not self.is_fitted:
            raise ValueError("Model not trained yet. Call train() first.")
        
        print("\n📈 Evaluating model...")
        
        # Encode test labels
        y_test_encoded = y_test.map(self.label_info['label_to_idx'])
        
        # Vectorize test texts
        X_test_vectors = self.vectorizer.transform(X_test)
        
        # Get predictions
        y_pred = self.model.predict(X_test_vectors)
        
        # Decode predictions back to label names
        y_pred_labels = [self.label_info['idx_to_label'][idx] for idx in y_pred]
        
        # Calculate metrics
        accuracy = accuracy_score(y_test_encoded, y_pred)
        precision = precision_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
        recall = recall_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test_encoded, y_pred, average='weighted', zero_division=0)
        
        print(f"  Accuracy:  {accuracy:.3f}")
        print(f"  Precision: {precision:.3f}")
        print(f"  Recall:    {recall:.3f}")
        print(f"  F1 Score:  {f1:.3f}")
        
        # Per-class metrics
        print("\n📊 Per-Class Performance:")
        print("-" * 60)
        print(classification_report(
            y_test_encoded, y_pred,
            target_names=self.label_info['unique_labels'],
            zero_division=0
        ))
        
        # Confusion matrix
        cm = confusion_matrix(y_test_encoded, y_pred)
        
        return {
            'accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'confusion_matrix': cm,
            'y_pred_labels': y_pred_labels,
            'y_test': y_test.values,
        }
    
    
    def plot_confusion_matrix(self, eval_results: Dict) -> None:
        """
        Plot confusion matrix heatmap.
        
        Args:
            eval_results: Dictionary from evaluate() method
        """
        
        cm = eval_results['confusion_matrix']
        labels = self.label_info['unique_labels']
        
        plt.figure(figsize=(12, 10))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d',
            cmap='Blues',
            xticklabels=labels,
            yticklabels=labels,
            cbar_kws={'label': 'Count'}
        )
        plt.title('Confusion Matrix - Interest Classification')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.show()
    
    
    def save_model(self, filepath: str) -> None:
        """
        Save trained model and vectorizer to disk.
        
        Args:
            filepath: Path to save model (without extension)
        """
        
        if not self.is_fitted:
            raise ValueError("Cannot save untrained model.")
        
        # Save vectorizer
        with open(f"{filepath}_vectorizer.pkl", 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        # Save model
        with open(f"{filepath}_model.pkl", 'wb') as f:
            pickle.dump(self.model, f)
        
        # Save label info
        with open(f"{filepath}_labels.pkl", 'wb') as f:
            pickle.dump(self.label_info, f)
        
        print(f"✓ Model saved to {filepath}_*.pkl")
    
    
    @staticmethod
    def load_model(filepath: str) -> 'InterestClassifier':
        """
        Load trained model and vectorizer from disk.
        
        Args:
            filepath: Path to model files (without extension)
        
        Returns:
            Loaded InterestClassifier instance
        """
        
        # Load label info first
        with open(f"{filepath}_labels.pkl", 'rb') as f:
            label_info = pickle.load(f)
        
        # Create classifier instance
        classifier = InterestClassifier(label_info)
        
        # Load vectorizer
        with open(f"{filepath}_vectorizer.pkl", 'rb') as f:
            classifier.vectorizer = pickle.load(f)
        
        # Load model
        with open(f"{filepath}_model.pkl", 'rb') as f:
            classifier.model = pickle.load(f)
        
        classifier.is_fitted = True
        
        print(f"✓ Model loaded from {filepath}_*.pkl")
        return classifier
    
    
    def get_feature_importance(self, top_n: int = 15) -> Dict[str, list]:
        """
        Get most important features (words/phrases) per class.
        
        Args:
            top_n: Number of top features to return per class
        
        Returns:
            Dictionary mapping labels to their top features
        """
        
        if not self.is_fitted:
            raise ValueError("Model not trained yet.")
        
        feature_names = np.array(self.vectorizer.get_feature_names_out())
        
        # Coefficients shape: (num_classes, num_features)
        coefficients = self.model.coef_
        
        feature_importance = {}
        
        for idx, label in self.label_info['idx_to_label'].items():
            # Get top positive and negative coefficients
            top_indices = np.argsort(coefficients[idx])[-top_n:][::-1]
            top_features = feature_names[top_indices]
            top_scores = coefficients[idx][top_indices]
            
            feature_importance[label] = {
                'features': top_features.tolist(),
                'scores': top_scores.tolist(),
            }
        
        return feature_importance


def train_and_evaluate_model(train_df: pd.DataFrame, test_df: pd.DataFrame, 
                            label_info: Dict) -> Tuple[InterestClassifier, Dict]:
    """
    Complete training and evaluation pipeline.
    
    Args:
        train_df: Training DataFrame with 'text' and 'label' columns
        test_df: Test DataFrame with 'text' and 'label' columns
        label_info: Label metadata dictionary
    
    Returns:
        Trained classifier and evaluation results
    """
    
    print("\n" + "="*60)
    print("TRAINING BASELINE CLASSIFIER")
    print("="*60)
    
    # Create classifier
    classifier = InterestClassifier(label_info)
    
    # Train
    classifier.train(train_df['text'], train_df['label'])
    
    # Evaluate
    eval_results = classifier.evaluate(test_df['text'], test_df['label'])
    
    return classifier, eval_results


# Example usage
if __name__ == "__main__":
    from ml_preprocessing import load_and_prepare_dataset, preprocess_data, show_class_distribution
    
    # Load and prepare data
    train_df, test_df, label_info = load_and_prepare_dataset()
    train_df, test_df = preprocess_data(train_df, test_df)
    show_class_distribution(train_df)
    
    # Train model
    classifier, eval_results = train_and_evaluate_model(train_df, test_df, label_info)
    
    # Plot confusion matrix
    classifier.plot_confusion_matrix(eval_results)
    
    # Show feature importance
    print("\n🔍 Top Features per Category:")
    feature_imp = classifier.get_feature_importance(top_n=5)
    for label, info in feature_imp.items():
        print(f"\n{label}:")
        for feat, score in zip(info['features'], info['scores']):
            print(f"  • {feat:20} ({score:+.3f})")
