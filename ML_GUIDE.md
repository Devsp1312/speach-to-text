"""
ML CLASSIFIER GUIDE
===================

Complete guide for the interest classification baseline model.

📁 File Structure:
  ml_preprocessing.py  - Data loading, cleaning, class distribution
  ml_classifier.py     - Model training, evaluation, feature importance
  ml_inference.py      - Predictions, long transcripts, profiles
  ml_example.py        - Complete demo (start here!)
  requirements_ml.txt  - Python dependencies

🚀 Quick Start:

1. Install dependencies:
   pip install scikit-learn pandas numpy matplotlib seaborn

2. Run the complete demo:
   python ml_example.py

3. This will:
   ✓ Load 20 Newsgroups dataset
   ✓ Map to 7 interest categories
   ✓ Train TF-IDF + Logistic Regression
   ✓ Show evaluation metrics
   ✓ Demo single predictions
   ✓ Demo long transcript handling
   ✓ Demo batch predictions
   ✓ Save trained model


═══════════════════════════════════════════════════════════════════════════════
1. DATA LOADING & PREPROCESSING (ml_preprocessing.py)
═══════════════════════════════════════════════════════════════════════════════

Dataset: 20 Newsgroups
  - Why: Real conversational text (forum posts)
  - Size: ~11,300 training + ~7,500 test samples
  - Format: Text documents with topic labels
  - License: Public domain

Category Mapping (20 Newsgroups → 7 Interests):

  Tech/Engineering ← comp.graphics, comp.windows.x, sci.electronics, sci.crypt...
  Academics/School ← talk.politics.*, talk.religion.*
  Career/Jobs ← misc.forsale
  Sports/Fitness ← rec.autos, rec.sport.*
  Entertainment/Gaming ← rec.motorcycles, alt.atheism
  Social/People ← talk.politics.*
  Food ← sci.space, comp.software (placeholder)

Key Functions:
  load_and_prepare_dataset()
    - Loads train/test split
    - Maps to 7 categories
    - Returns cleaned DataFrames

  preprocess_data(train_df, test_df)
    - Lowercases text
    - Removes extra whitespace
    - Removes empty samples
    - Returns cleaned data

  show_class_distribution(df)
    - Prints distribution visualization
    - Shows count and percentage per class


═══════════════════════════════════════════════════════════════════════════════
2. MODEL TRAINING (ml_classifier.py)
═══════════════════════════════════════════════════════════════════════════════

Architecture:

  [Text Input] 
       ↓
   [TfidfVectorizer]
       ↓ (creates sparse matrix)
   [Logistic Regression]
       ↓
   [Probability Scores]

TfidfVectorizer Configuration:
  - lowercase: True
    Why: Normalize case sensitivity (TECH = tech = Tech)
  
  - ngram_range: (1, 2)
    Why: Capture both single words and common phrases
    Example: "machine learning" as one feature
  
  - min_df: 2
    Why: Ignore words in <2 documents (removes noise)
  
  - max_df: 0.9
    Why: Ignore words in >90% of documents (removes common words)
  
  - max_features: 50,000
    Why: Limit vocabulary size for speed & memory

LogisticRegression Configuration:
  - max_iter: 1000
    Why: Ensure convergence (dataset is large)
  
  - class_weight: 'balanced'
    Why: Handle class imbalance (not all interests equally common)
  
  - random_state: 42
    Why: Reproducibility

Key Classes:
  
  InterestClassifier
    - train(X_train, y_train)
      • Vectorizes text with TF-IDF
      • Fits logistic regression
      • Returns training accuracy
    
    - evaluate(X_test, y_test)
      • Computes accuracy, precision, recall, F1
      • Generates confusion matrix
      • Returns per-class metrics
    
    - get_feature_importance(top_n=15)
      • Shows most important words per class
      • Useful for interpretation & debugging
    
    - save_model(filepath) / load_model(filepath)
      • Persistence for production


═══════════════════════════════════════════════════════════════════════════════
3. INFERENCE & PREDICTIONS (ml_inference.py)
═══════════════════════════════════════════════════════════════════════════════

Single Prediction:

  predictor = InterestPredictor(classifier)
  result = predictor.predict_single("I love coding and AI")
  
  Returns:
  {
    'primary': 'Tech/Engineering',
    'confidence': 0.78,
    'all_predictions': [
      {'interest': 'Tech/Engineering', 'confidence': 0.78},
      {'interest': 'Academics/School', 'confidence': 0.15},
      {'interest': 'Career/Jobs', 'confidence': 0.07}
    ],
    'interpretation': 'High confidence in Tech/Engineering interest.'
  }

Confidence Threshold:
  - Default: 0.45 (45%)
  - If top prediction < 0.45 → "Unknown / Low Signal"
  - User configurable: predictor.confidence_threshold = 0.5

Long Transcript Handling:

  Input: 5-minute conversation (2000+ words)
  
  Process:
    1. Split into chunks (~150 words each)
    2. Overlap chunks by 75% (smooth transitions)
    3. Predict interests for each chunk
    4. Average probabilities across chunks
    5. Return aggregated profile
  
  Example:
    profile = predictor.predict_long_transcript(long_text)
    
    Returns:
    {
      'primary': 'Entertainment/Gaming',
      'top_confidence': 0.65,
      'all_interests': [
        {'interest': 'Entertainment/Gaming', 'confidence': 0.65},
        {'interest': 'Social/People', 'confidence': 0.20},
        ...
      ],
      'chunks_analyzed': 8,
      'total_words': 1847
    }

Why Chunking Works:
  - Mimics human impression formation (gradual, not instantaneous)
  - Handles mixed-topic conversations naturally
  - Reduces noise from single off-topic sentences
  - Enables real-time processing of long streams
  - More robust than single long-document prediction

Batch Predictions:

  results = batch_predict(predictor, [text1, text2, text3])
  df = create_prediction_dataframe(predictor, texts)


═══════════════════════════════════════════════════════════════════════════════
4. EVALUATION METRICS
═══════════════════════════════════════════════════════════════════════════════

What They Mean:

  Accuracy: (TP + TN) / Total
    - Proportion of correct predictions
    - Good for balanced datasets
    - Example: 85% of predictions were correct
  
  Precision: TP / (TP + FP)
    - Of predicted positives, how many are correct?
    - "When I predict Tech, how often am I right?"
    - High precision = fewer false alarms
  
  Recall: TP / (TP + FN)
    - Of actual positives, how many did we catch?
    - "Did I find all the Tech people?"
    - High recall = fewer missed cases
  
  F1 Score: 2 * (Precision * Recall) / (Precision + Recall)
    - Harmonic mean of precision & recall
    - Balanced metric for imbalanced data
    - Good for comparisons

Confusion Matrix:
  - Shows which classes get confused
  - Example: Are "Career/Jobs" often confused with "Tech/Engineering"?
  - Helps identify improvement areas


═══════════════════════════════════════════════════════════════════════════════
5. WHY THIS IS A STRONG BASELINE
═══════════════════════════════════════════════════════════════════════════════

✅ Strengths:

1. Interpretable
   - See which words drive each prediction
   - Understand model decisions (not black-box)
   - Easy to debug and improve
   
2. Fast
   - Vectorization: milliseconds
   - Inference: <10ms per sample
   - Can process real-time transcripts
   
3. Robust
   - Balanced class weights handle imbalance
   - Works well with variable-length text
   - Confidence scores for uncertainty
   
4. Practical
   - No complex hyperparameter tuning
   - Easy to deploy and update
   - Low computational requirements
   
5. Scalable
   - Works with small datasets (100s samples)
   - Can handle millions of samples
   - Memory efficient

⚠️  Limitations:

1. No Context Understanding
   - "I hate math" → might predict Academics (misses negation)
   - Sarcasm detection impossible
   - Depends purely on word co-occurrence
   
2. Fixed Categories
   - Can't discover new interest types
   - Requires manual category mapping
   - Inflexible for new domains
   
3. No Personalization
   - Same model for all users
   - Can't adapt to individual patterns
   - No user history tracking
   
4. Domain Dependency
   - Trained on forum discussions
   - Might not work on other text types
   - Requires retraining for new domains

🚀 Future Improvements:

1. Fine-tune BERT/RoBERTa on actual transcripts
   - Captures semantic meaning, not just words
   - Handles context, negation, sarcasm
   - Better performance on short texts
   
2. Hierarchical interests
   - Tech → AI → NLP, Robotics
   - Career → Tech Jobs, Sales, Management
   - More nuanced profiling
   
3. Active learning
   - Model improves as you collect real data
   - Request user feedback on uncertain cases
   - Continuous improvement loop
   
4. Multi-label classification
   - Users can have multiple primary interests
   - Interest intensity (1-10 scale)
   - More realistic than single-label
   
5. User feedback loop
   - Users correct misclassifications
   - Personalized re-ranking
   - A/B testing different models


═══════════════════════════════════════════════════════════════════════════════
6. INTEGRATION WITH STREAMLIT APP
═══════════════════════════════════════════════════════════════════════════════

Option 1: Replace keyword matching (current)

  Instead of:
    interests = score_interests(cleaned_text)
  
  Use:
    from ml_inference import InterestPredictor
    predictor = InterestPredictor(classifier)
    result = predictor.predict_single(cleaned_text)
    interests = {p['interest']: p['confidence']*100 
                 for p in result['all_predictions']}

Option 2: Add as alternative mode

  # In sidebar
  prediction_method = st.radio(
    "Prediction method:",
    ["Keyword-based", "ML Classifier", "Hybrid"]
  )
  
  if prediction_method == "ML Classifier":
    # Use predictor

Option 3: Ensemble (best)

  # Combine both methods
  keyword_scores = score_interests(text)
  ml_scores = predictor.predict_single(text)
  
  # Weighted average
  combined = 0.4 * keyword_scores + 0.6 * ml_scores


═══════════════════════════════════════════════════════════════════════════════
7. TROUBLESHOOTING
═══════════════════════════════════════════════════════════════════════════════

Problem: Model predicts same interest every time
  Solution: Check if top_confidence is below threshold
           Verify training data has balanced classes
           Try lowering confidence_threshold

Problem: Predictions don't make sense
  Solution: Check top features (get_feature_importance)
           Review raw text (check for preprocessing issues)
           Verify label mapping is correct

Problem: Very slow inference
  Solution: Use vectorizer.transform (not fit_transform)
           Pre-compute common phrases as features
           Batch predictions when possible

Problem: Low accuracy
  Solution: Check class distribution (too imbalanced?)
           Increase training data
           Verify label mapping accuracy
           Consider fine-tuning hyperparameters


═══════════════════════════════════════════════════════════════════════════════
8. CODE EXAMPLES
═══════════════════════════════════════════════════════════════════════════════

Example 1: Train and save model

  from ml_preprocessing import load_and_prepare_dataset, preprocess_data
  from ml_classifier import train_and_evaluate_model
  
  # Load data
  train_df, test_df, label_info = load_and_prepare_dataset()
  train_df, test_df = preprocess_data(train_df, test_df)
  
  # Train
  classifier, results = train_and_evaluate_model(train_df, test_df, label_info)
  
  # Save
  classifier.save_model("my_classifier")

Example 2: Load and predict

  from ml_classifier import InterestClassifier
  from ml_inference import InterestPredictor
  
  # Load
  classifier = InterestClassifier.load_model("my_classifier")
  predictor = InterestPredictor(classifier)
  
  # Predict
  result = predictor.predict_single("I love programming")
  print(result['primary'], result['confidence'])

Example 3: Long transcript

  long_text = """
  So I started learning Python last month...
  [1000+ more words...]
  """
  
  profile = predictor.predict_long_transcript(long_text)
  print(f"Main interest: {profile['primary']}")
  print(f"Confidence: {profile['top_confidence']:.1%}")

Example 4: Batch analysis

  texts = [...]  # List of 100 transcripts
  df = create_prediction_dataframe(predictor, texts)
  print(df.describe())
  print(df['primary_interest'].value_counts())


═══════════════════════════════════════════════════════════════════════════════
9. NEXT STEPS
═══════════════════════════════════════════════════════════════════════════════

For Your Capstone:

1. Evaluate on your own transcripts
   - Does it work better than keyword matching?
   - Which cases does it fail on?
   
2. Collect human labels
   - Have people manually classify 100 transcripts
   - Compare vs model predictions
   - Identify systematic errors
   
3. Fine-tune on real data
   - Retrain with labeled transcripts
   - Should improve accuracy significantly
   
4. Deploy as API
   - Flask/FastAPI endpoint
   - Docker container
   - Cloud deployment (AWS/GCP)
   
5. Monitor in production
   - Track prediction confidence
   - Log misclassifications
   - Detect distribution shift

6. Document everything
   - How did you train it?
   - What dataset did you use?
   - How confident should users be?
   - What are the limitations?

Good luck with your capstone! 🚀
"""
