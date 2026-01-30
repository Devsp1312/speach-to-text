"""
Quick Demo - No Network Required
==================================

This script demonstrates the ML classifier without needing to download data.
Uses a small mock dataset instead.
"""

print("""
╔════════════════════════════════════════════════════════════════╗
║           BASELINE CLASSIFIER - QUICK DEMO                    ║
║                  (No internet required)                        ║
╚════════════════════════════════════════════════════════════════╝
""")

from ml_classifier import InterestClassifier
from ml_inference import InterestPredictor
import pandas as pd

# Create a small mock dataset for demo
print("\n📊 Creating mock dataset...")

mock_data = {
    'text': [
        'I love programming and machine learning algorithms',
        'Sports and fitness keep me healthy and active',
        'Gaming tournaments are exciting and competitive',
        'I study computer science and artificial intelligence',
        'Cooking shows and recipes inspire my culinary skills',
        'Social events and networking are important to me',
        'Career advancement in tech is my priority',
        'I play basketball and run marathons',
        'Video games and esports are my passion',
        'School projects and research papers keep me busy',
    ],
    'label': [
        'Tech/Engineering',
        'Sports/Fitness',
        'Entertainment/Gaming',
        'Academics/School',
        'Food',
        'Social/People',
        'Career/Jobs',
        'Sports/Fitness',
        'Entertainment/Gaming',
        'Academics/School',
    ]
}

df = pd.DataFrame(mock_data)
print(f"✓ Created {len(df)} samples across 7 categories")

# Create label info
label_info = {
    'unique_labels': sorted(df['label'].unique().tolist()),
    'label_to_idx': {label: idx for idx, label in enumerate(sorted(df['label'].unique()))},
    'idx_to_label': {idx: label for idx, label in enumerate(sorted(df['label'].unique()))},
    'num_classes': len(df['label'].unique()),
}

print(f"✓ Classes: {', '.join(label_info['unique_labels'])}")

# Train classifier on mock data
print("\n🔄 Training classifier on mock data...")
classifier = InterestClassifier(label_info)

# For small datasets, adjust TF-IDF settings
classifier.vectorizer.min_df = 1  # Changed from 2
classifier.vectorizer.max_df = 1.0  # Changed from 0.9

classifier.train(df['text'], df['label'])

# Evaluate on same data (just for demo)
print("\n📈 Evaluation Results:")
eval_results = classifier.evaluate(df['text'], df['label'])

print(f"""
  Accuracy:  {eval_results['accuracy']:.1%}
  Precision: {eval_results['precision']:.1%}
  Recall:    {eval_results['recall']:.1%}
  F1 Score:  {eval_results['f1']:.1%}
""")

# Make predictions
print("\n" + "="*60)
print("SINGLE PREDICTION DEMO")
print("="*60)

predictor = InterestPredictor(classifier)

test_texts = [
    "I just started learning Python and love coding!",
    "Just finished my 10-mile run!",
    "Spent all day gaming and streaming esports tournaments",
]

for text in test_texts:
    print(f"\n📄 \"{text}\"")
    result = predictor.predict_single(text)
    print(f"   → Primary: {result['primary']}")
    print(f"   → Confidence: {result['confidence']:.0%}")
    print(f"   → Top 3:")
    for pred in result['all_predictions'][:3]:
        print(f"      • {pred['interest']:25} {pred['confidence']:.0%}")

# Feature importance
print("\n" + "="*60)
print("TOP FEATURES (What words drive predictions?)")
print("="*60)

try:
    features = classifier.get_feature_importance(top_n=3)
    for label in sorted(features.keys()):
        feats = features[label]['features']
        print(f"\n{label}:")
        for feat in feats:
            print(f"  • {feat}")
except Exception as e:
    print(f"Feature analysis: {e}")

# Save model
print("\n" + "="*60)
print("SAVING MODEL")
print("="*60)

try:
    classifier.save_model("demo_classifier")
    print("✓ Model saved! Files created:")
    print("  • demo_classifier_model.pkl")
    print("  • demo_classifier_vectorizer.pkl")
    print("  • demo_classifier_labels.pkl")
except Exception as e:
    print(f"Save error: {e}")

print("\n" + "="*60)
print("✅ DEMO COMPLETE!")
print("="*60)

print("""
Next Steps:

1. Run this demo anytime with:
   /usr/local/bin/python3 quick_demo.py

2. To use the real dataset:
   /usr/local/bin/python3 ml_example.py
   (Requires internet connection)

3. To integrate into your Streamlit app:
   Read INTEGRATION_GUIDE.md

4. Create Python alias to use 'python' command:
   echo 'alias python=/usr/local/bin/python3' >> ~/.zshrc
   source ~/.zshrc

✨ You've got it working! 🚀
""")
