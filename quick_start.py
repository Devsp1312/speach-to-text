"""
QUICK START: Train & Use ML Classifier in 5 Minutes
====================================================

Copy-paste friendly script to:
1. Install dependencies
2. Train the model
3. Test predictions
4. Save for your app

Run with: python quick_start.py
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║           BASELINE CLASSIFIER - QUICK START                   ║
║                                                                ║
║  This script will:                                             ║
║  1. Load 20 Newsgroups dataset (~11k samples)                 ║
║  2. Train TF-IDF + Logistic Regression                        ║
║  3. Evaluate model (accuracy, F1, etc)                        ║
║  4. Test on sample texts                                      ║
║  5. Save model for Streamlit app                              ║
║                                                                ║
║  Time: ~3-5 minutes (first run, includes download)            ║
║  Time: ~10 seconds (cached runs)                              ║
╚════════════════════════════════════════════════════════════════╝
""")

# ==============================================================================
# IMPORTS
# ==============================================================================

import sys

try:
    from ml_preprocessing import load_and_prepare_dataset, preprocess_data, show_class_distribution
    from ml_classifier import train_and_evaluate_model
    from ml_inference import InterestPredictor
except ImportError as e:
    print(f"❌ Error: {e}")
    print("\nMake sure all files are in the same directory:")
    print("  - ml_preprocessing.py")
    print("  - ml_classifier.py")
    print("  - ml_inference.py")
    sys.exit(1)


# ==============================================================================
# STEP 1: LOAD & PREPARE DATA
# ==============================================================================

print("\n" + "="*70)
print("STEP 1: Loading & Preparing Data")
print("="*70)

train_df, test_df, label_info = load_and_prepare_dataset(random_state=42)
train_df, test_df = preprocess_data(train_df, test_df)

print(f"\n✓ Loaded {len(train_df)} training + {len(test_df)} test samples")
print(f"✓ Classes: {label_info['num_classes']}")

show_class_distribution(train_df)


# ==============================================================================
# STEP 2: TRAIN MODEL
# ==============================================================================

print("\n" + "="*70)
print("STEP 2: Training Model")
print("="*70)

classifier, eval_results = train_and_evaluate_model(train_df, test_df, label_info)


# ==============================================================================
# STEP 3: SHOW RESULTS
# ==============================================================================

print("\n" + "="*70)
print("STEP 3: Evaluation Results")
print("="*70)

print(f"""
📊 Model Performance:
   • Accuracy:  {eval_results['accuracy']:.1%}
   • Precision: {eval_results['precision']:.1%}
   • Recall:    {eval_results['recall']:.1%}
   • F1 Score:  {eval_results['f1']:.1%}

What this means:
   ✓ Accuracy: Correct predictions on random test samples
   ✓ Precision: When we predict an interest, how often are we right?
   ✓ Recall: Did we catch all the samples of that interest?
   ✓ F1: Balanced score (best for imbalanced data)
""")


# ==============================================================================
# STEP 4: TEST ON SAMPLE TEXTS
# ==============================================================================

print("\n" + "="*70)
print("STEP 4: Testing on Sample Texts")
print("="*70)

predictor = InterestPredictor(classifier)

samples = [
    "I love programming and machine learning",
    "Sports and fitness are my passion",
    "Gaming and entertainment all day",
    "I study academics and science",
]

for sample in samples:
    print(f"\n📄 \"{sample}\"")
    result = predictor.predict_single(sample)
    print(f"   → {result['primary']} ({result['confidence']:.0%})")


# ==============================================================================
# STEP 5: TEST LONG TRANSCRIPT
# ==============================================================================

print("\n" + "="*70)
print("STEP 5: Testing Long Transcript")
print("="*70)

long_text = """
I've been really into gaming lately, especially competitive esports.
I play strategy games and watch tournaments online all the time.
My friends and I organize gaming meetups regularly.
We also discuss tech and hardware for gaming setups.
Besides gaming, I enjoy socializing and meeting people in the gaming community.
It's the best combination of strategy, competition, and social interaction.
"""

profile = predictor.predict_long_transcript(long_text)

print(f"""
📊 Long Transcript Results:
   Primary Interest: {profile['primary']}
   Confidence: {profile['top_confidence']:.0%}
   
   Top interests:
""")

for interest in profile['all_interests'][:3]:
    print(f"   • {interest['interest']:25} {interest['confidence']:.0%}")


# ==============================================================================
# STEP 6: TOP FEATURES
# ==============================================================================

print("\n" + "="*70)
print("STEP 6: Top Features per Category (Explainability)")
print("="*70)

features = classifier.get_feature_importance(top_n=3)

print("\n🔍 What words drive each prediction?\n")
for label in sorted(features.keys()):
    feats = features[label]['features']
    print(f"{label}:")
    for feat in feats:
        print(f"  • {feat}")
    print()


# ==============================================================================
# STEP 7: SAVE MODEL
# ==============================================================================

print("\n" + "="*70)
print("STEP 7: Saving Model")
print("="*70)

classifier.save_model("interest_classifier")

print("""
✓ Model saved successfully!

Files created:
  • interest_classifier_model.pkl     (Logistic Regression)
  • interest_classifier_vectorizer.pkl (TF-IDF Vectorizer)
  • interest_classifier_labels.pkl     (Class mappings)

Now you can use in Streamlit:
  from ml_classifier import InterestClassifier
  from ml_inference import InterestPredictor
  
  classifier = InterestClassifier.load_model("interest_classifier")
  predictor = InterestPredictor(classifier)
  result = predictor.predict_single("your text here")
""")


# ==============================================================================
# DONE
# ==============================================================================

print("\n" + "="*70)
print("✅ COMPLETE!")
print("="*70)

print("""
Next steps:

1. Review the model (check top features above)
2. Test on your own text samples
3. Integrate into Streamlit app (see INTEGRATION_GUIDE.md)
4. Monitor predictions in production
5. Collect feedback to improve model

Questions? See:
  • ML_GUIDE.md - Detailed documentation
  • INTEGRATION_GUIDE.md - How to use in Streamlit
  • ml_example.py - Full code walkthrough

Good luck! 🚀
""")
