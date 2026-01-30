"""
Complete Example & Demo
=======================

This script demonstrates the full pipeline:
1. Load and prepare data
2. Train the baseline classifier
3. Evaluate on test set
4. Make inference on new text
5. Handle long transcripts
6. Generate user profiles

Ready for Google Colab or local execution.
"""

import pandas as pd
import numpy as np
from ml_preprocessing import (
    load_and_prepare_dataset, 
    preprocess_data, 
    show_class_distribution
)
from ml_classifier import train_and_evaluate_model
from ml_inference import InterestPredictor, create_prediction_dataframe


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)


def demo_single_predictions(predictor: InterestPredictor) -> None:
    """Demo single text predictions."""
    
    print_section("DEMO 1: Single Text Predictions")
    
    test_samples = [
        "I love coding and building web applications. Machine learning fascinates me.",
        "Sports are my passion. I play basketball and run marathons regularly.",
        "I enjoy cooking, trying new recipes, and exploring different cuisines.",
        "Science is amazing. I read about physics and space exploration every day.",
        "Gaming is life. I play competitive shooters and watch esports tournaments.",
    ]
    
    for i, text in enumerate(test_samples, 1):
        print(f"\n📄 Sample {i}:")
        print(f"Text: \"{text}\"")
        result = predictor.predict_single(text)
        print(f"Primary: {result['primary']}")
        print(f"Confidence: {result['confidence']:.1%}")
        print("Top 3 predictions:")
        for j, pred in enumerate(result['all_predictions'][:3], 1):
            print(f"  {j}. {pred['interest']:25} {pred['confidence']:6.1%}")


def demo_long_transcript(predictor: InterestPredictor) -> None:
    """Demo long transcript handling."""
    
    print_section("DEMO 2: Long Transcript (5-minute conversation)")
    
    # Mock 5-minute transcript
    long_transcript = """
    So I've been really into gaming lately, particularly competitive esports and strategy games.
    I play a lot of complex strategy games and I'm always watching tournaments online.
    But I also really enjoy social activities - going out with friends, meeting new people at gaming events.
    I think what draws me most is the combination of strategic thinking and the community aspect.
    My friends joke that I'm always talking about new games or organizing gaming meetups.
    
    Besides gaming, I've been learning some basic programming to create game mods.
    I took an online course in Python and I'm working on my first project.
    Technology really interests me - I follow tech news and new hardware releases.
    But honestly, games are still my primary focus. They combine everything I love:
    technology, strategy, competition, and socializing with people who share my interests.
    
    I also try to stay healthy though. I go to the gym a few times a week.
    I need to balance my gaming with some physical activity. Can't be a full couch potato!
    Sometimes I'll play games with people I meet at the gym, which is fun.
    It's interesting how hobbies can overlap and connect different parts of your life.
    """
    
    # Make prediction
    profile = predictor.predict_long_transcript(long_transcript, words_per_chunk=150)
    
    # Display results
    print("\n📊 Aggregated Profile Results:")
    print(f"Primary Interest: {profile['primary']}")
    print(f"Confidence: {profile['top_confidence']:.1%}")
    print(f"\nInterpretation: {profile['interpretation']}")
    print(f"\nChunks analyzed: {profile['chunks_analyzed']}")
    print(f"Total words: {profile['total_words']}")
    
    print("\nAll interests (averaged across chunks):")
    for i, item in enumerate(profile['all_interests'], 1):
        confidence_pct = item['confidence'] * 100
        bar_length = int(confidence_pct / 5)
        bar = "█" * bar_length
        print(f"{i}. {item['interest']:25} {confidence_pct:5.1f}% {bar}")


def demo_batch_predictions(predictor: InterestPredictor) -> None:
    """Demo batch prediction with DataFrame output."""
    
    print_section("DEMO 3: Batch Predictions on Multiple Texts")
    
    # Create sample dataset
    sample_texts = [
        "Python programming and web development are my passion.",
        "I'm a fitness coach helping people achieve their health goals.",
        "AI and machine learning are changing the world.",
        "I love organizing social events and meeting new people.",
        "Playing video games is the best way to relax after work.",
        "Academic research in neuroscience interests me deeply.",
        "Cooking shows and food blogs are my favorite entertainment.",
        "I compete in triathlon competitions every season.",
    ]
    
    # Make predictions
    print(f"Making predictions on {len(sample_texts)} samples...")
    df = create_prediction_dataframe(predictor, sample_texts)
    
    # Display DataFrame
    print("\n📋 Prediction Results:")
    print(df.to_string(index=False))
    
    # Summary statistics
    print("\n📈 Summary Statistics:")
    interest_counts = df['primary_interest'].value_counts()
    for interest, count in interest_counts.items():
        pct = (count / len(df)) * 100
        print(f"  {interest:25} {count:2} samples ({pct:5.1f}%)")


def print_model_interpretation(classifier, eval_results) -> None:
    """Print interpretation of model results."""
    
    print_section("MODEL INTERPRETATION & INSIGHTS")
    
    print("""
✅ WHY THIS APPROACH IS A STRONG BASELINE:

1. TF-IDF + Logistic Regression
   - Fast training and inference (milliseconds for single predictions)
   - Highly interpretable - can see which words drive each prediction
   - Robust baseline that outperforms naive approaches
   - No complex hyperparameter tuning needed
   
2. Balanced Class Weights
   - Prevents bias toward majority classes
   - Handles imbalanced interest distributions
   - Fair performance across all 7 interest categories
   
3. Confidence Scoring
   - Provides probabilities, not just hard predictions
   - "Unknown / Low Signal" handling for uncertain cases
   - Users can see confidence levels for each prediction
   
4. Long Transcript Handling
   - Chunks ~150-word segments with 75% overlap
   - Averages predictions across chunks
   - Robust to conversational noise and topic shifts
   - Mimics how humans gradually form impressions
   
5. Scalability
   - Can process real-time transcripts as they arrive
   - No need to wait for complete audio file
   - Works with partial conversations

6. Interpretability (ML Ops!)
   - Feature importance shows what drives decisions
   - Easy to debug why user got classified as X
   - Can adjust weights or add custom rules
   - Audit trail for fairness/bias checking

⚠️  LIMITATIONS & FUTURE IMPROVEMENTS:

   - Doesn't understand context (just co-occurrence)
   - Can't handle sarcasm or implied meanings
   - Fixed 7 categories (can't discover new interests)
   - Needs manual dataset mapping
   - No personalization across users
   
   → Future: Fine-tune a transformer (BERT) on actual transcripts
   → Add hierarchical interests (Tech → AI → NLP)
   → Implement active learning to improve with real data
    """)


def main():
    """Run complete demo pipeline."""
    
    print("\n" + "▀"*70)
    print("  🎓 CAPSTONE PROJECT: INTEREST CLASSIFICATION BASELINE")
    print("  TF-IDF + Logistic Regression Pipeline")
    print("▀"*70)
    
    # ============================================================================
    # STEP 1: Load and prepare data
    # ============================================================================
    print_section("STEP 1: Loading & Preparing Data")
    
    train_df, test_df, label_info = load_and_prepare_dataset(random_state=42)
    print(f"\n✓ Loaded dataset:")
    print(f"  • Training samples: {len(train_df)}")
    print(f"  • Test samples: {len(test_df)}")
    print(f"  • Classes: {label_info['num_classes']}")
    
    train_df, test_df = preprocess_data(train_df, test_df)
    show_class_distribution(train_df, "Training Data Distribution")
    
    
    # ============================================================================
    # STEP 2: Train model
    # ============================================================================
    print_section("STEP 2: Training Baseline Classifier")
    
    classifier, eval_results = train_and_evaluate_model(train_df, test_df, label_info)
    
    # Print key metrics
    print("\n📊 Key Metrics:")
    print(f"  • Accuracy:  {eval_results['accuracy']:.1%}")
    print(f"  • Precision: {eval_results['precision']:.1%}")
    print(f"  • Recall:    {eval_results['recall']:.1%}")
    print(f"  • F1 Score:  {eval_results['f1']:.1%}")
    
    
    # ============================================================================
    # STEP 3: Feature importance
    # ============================================================================
    print_section("STEP 3: Feature Importance (Top Words per Category)")
    
    feature_imp = classifier.get_feature_importance(top_n=5)
    for label in sorted(feature_imp.keys()):
        features = feature_imp[label]['features']
        print(f"\n{label}:")
        for feat in features:
            print(f"  • {feat}")
    
    
    # ============================================================================
    # STEP 4: Initialize predictor
    # ============================================================================
    predictor = InterestPredictor(classifier)
    
    
    # ============================================================================
    # STEP 5: Run demos
    # ============================================================================
    demo_single_predictions(predictor)
    demo_long_transcript(predictor)
    demo_batch_predictions(predictor)
    
    
    # ============================================================================
    # STEP 6: Print interpretation
    # ============================================================================
    print_model_interpretation(classifier, eval_results)
    
    
    # ============================================================================
    # STEP 7: Save model for later use
    # ============================================================================
    print_section("STEP 7: Saving Model")
    
    classifier.save_model("interest_classifier")
    print("\n✓ Model saved! Load later with:")
    print("   classifier = InterestClassifier.load_model('interest_classifier')")
    
    
    print_section("✅ DEMO COMPLETE")
    print("""
Next steps:
1. Try the predictor on your own text samples
2. Collect real transcript data to fine-tune
3. Deploy as an API or integrate into Streamlit app
4. Monitor predictions in production
5. Continuously improve with new data
    """)


if __name__ == "__main__":
    main()
