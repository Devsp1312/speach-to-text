"""
Integration Guide: Adding ML Classifier to Streamlit App
=========================================================

This file shows how to integrate the trained ML classifier into your
existing Streamlit app as an alternative to keyword-based scoring.

📌 Current Workflow (Keyword-based):
   
   Audio → Transcribe → Clean Text → Score Interests (keyword matching)
   
   └→ Limitations:
      - Misses interests not explicitly mentioned
      - Sarcasm/context not understood
      - Needs extensive keyword lists

📌 New Workflow (ML-based):
   
   Audio → Transcribe → Clean Text → Score Interests (ML model)
   
   └→ Benefits:
      - Learns patterns from data
      - Understands context better
      - Works with partial mentions


═══════════════════════════════════════════════════════════════════════════════
OPTION 1: Simple Replacement
═══════════════════════════════════════════════════════════════════════════════

In your interests.py, replace score_interests() with ML version:

  from ml_classifier import InterestClassifier
  from ml_inference import InterestPredictor
  
  # Load model once at startup (cached)
  @st.cache_resource
  def load_interest_model():
      classifier = InterestClassifier.load_model("interest_classifier")
      return InterestPredictor(classifier)
  
  predictor = load_interest_model()
  
  def score_interests(text):
      \"\"\"Score interests using ML model\"\"\"
      result = predictor.predict_single(text)
      
      # Convert to same format as keyword scoring
      scores = {}
      for pred in result['all_predictions']:
          scores[pred['interest']] = pred['confidence'] * 100
      
      return scores

Then your existing app.py doesn't need changes - it just uses the new scorer!


═══════════════════════════════════════════════════════════════════════════════
OPTION 2: Add ML as Alternative Mode
═══════════════════════════════════════════════════════════════════════════════

In app.py, add selector in sidebar:

  with st.sidebar:
      st.divider()
      scoring_method = st.radio(
          "Scoring Method:",
          ["🔑 Keyword-based", "🤖 ML Classifier"]
      )
  
  # ... rest of transcription code ...
  
  # When displaying results:
  if scoring_method == "🔑 Keyword-based":
      interest_scores = score_interests(cleaned)
  else:
      # Use ML
      from ml_inference import InterestPredictor
      result = predictor.predict_single(cleaned)
      interest_scores = {
          p['interest']: p['confidence'] * 100 
          for p in result['all_predictions']
      }


═══════════════════════════════════════════════════════════════════════════════
OPTION 3: Hybrid Approach (Recommended)
═══════════════════════════════════════════════════════════════════════════════

Combine both methods for best results:

  def score_interests_hybrid(text, weight_ml=0.6, weight_keyword=0.4):
      \"\"\"
      Ensemble: Keyword + ML
      
      Args:
          text: Cleaned text
          weight_ml: Weight for ML predictions (0-1)
          weight_keyword: Weight for keyword predictions (0-1)
      
      Returns:
          Dictionary of combined scores
      \"\"\"
      
      # Get keyword scores
      keyword_scores = score_interests_keyword(text)
      
      # Get ML scores
      ml_result = predictor.predict_single(text)
      ml_scores = {
          p['interest']: p['confidence'] * 100 
          for p in ml_result['all_predictions']
      }
      
      # Combine with weighted average
      combined = {}
      for interest in keyword_scores.keys():
          kw = keyword_scores.get(interest, 0)
          ml = ml_scores.get(interest, 0)
          combined[interest] = (weight_keyword * kw) + (weight_ml * ml)
      
      return combined

Benefits:
  - Catches interests both methods recognize (high confidence)
  - Provides fallback if one method fails
  - Balances precision (keywords) + recall (ML)


═══════════════════════════════════════════════════════════════════════════════
HANDLING LONG TRANSCRIPTS IN STREAMLIT
═══════════════════════════════════════════════════════════════════════════════

For multi-chunk audio (>5 min), use aggregate prediction:

  if len(transcript) > 1000:  # Long transcript
      with st.spinner("Analyzing long transcript..."):
          profile = predictor.predict_long_transcript(transcript)
      
      st.subheader("📊 Aggregated Profile")
      st.write(f"*Analyzed {profile['chunks_analyzed']} chunks*")
      
      col1, col2 = st.columns(2)
      with col1:
          st.metric("Dominant Interest", profile['primary'])
      with col2:
          st.metric("Confidence", f"{profile['top_confidence']:.0%}")
      
      # Show all interests
      st.write("Interest Distribution:")
      for item in profile['all_interests']:
          pct = item['confidence'] * 100
          st.write(f"• {item['interest']}: {pct:.0f}%")
  
  else:  # Short transcript
      result = predictor.predict_single(transcript)
      # ... display result ...


═══════════════════════════════════════════════════════════════════════════════
CACHING FOR PERFORMANCE
═══════════════════════════════════════════════════════════════════════════════

Key: Load model ONCE at startup, not every prediction!

  import streamlit as st
  from ml_classifier import InterestClassifier
  from ml_inference import InterestPredictor
  
  @st.cache_resource  # Cache the model
  def load_classifier():
      print("Loading classifier...")  # Prints only on startup
      return InterestClassifier.load_model("interest_classifier")
  
  @st.cache_resource
  def get_predictor():
      classifier = load_classifier()
      return InterestPredictor(classifier)
  
  # Use in app
  predictor = get_predictor()  # Fast! (cached)
  result = predictor.predict_single(text)  # <10ms

Performance:
  - First run: ~2 seconds (load model)
  - Subsequent runs: instant! (cached)


═══════════════════════════════════════════════════════════════════════════════
ADDING CONFIDENCE INDICATOR
═══════════════════════════════════════════════════════════════════════════════

Show users how confident the model is:

  result = predictor.predict_single(text)
  
  confidence = result['confidence']
  
  # Visual indicator
  if confidence > 0.7:
      st.success(f"✓ High confidence: {confidence:.0%}")
      explanation = "Model is very confident in this classification."
  elif confidence > 0.45:
      st.info(f"~ Medium confidence: {confidence:.0%}")
      explanation = "Classification is uncertain. Consider the alternatives below."
  else:
      st.warning(f"⚠ Low confidence: {confidence:.0%}")
      explanation = "Model couldn't confidently classify. Mixed interests detected."
  
  st.write(explanation)
  
  # Show all candidates
  st.write("Alternative classifications:")
  for pred in result['all_predictions']:
      st.write(f"• {pred['interest']}: {pred['confidence']:.0%}")


═══════════════════════════════════════════════════════════════════════════════
DEBUGGING: IF PREDICTIONS SEEM WRONG
═══════════════════════════════════════════════════════════════════════════════

1. Check model features:
   
   feature_imp = classifier.get_feature_importance(top_n=10)
   for label, info in feature_imp.items():
       st.write(f"{label}: {info['features']}")

2. Compare with keywords:
   
   col1, col2 = st.columns(2)
   with col1:
       keyword_result = score_interests_keyword(text)
       st.write("Keyword scores:", keyword_result)
   with col2:
       ml_result = predictor.predict_single(text)
       st.write("ML scores:", ml_result)

3. Check text cleaning:
   
   st.write("Original:", text[:200])
   st.write("Cleaned:", clean_text(text)[:200])


═══════════════════════════════════════════════════════════════════════════════
EXAMPLE: COMPLETE STREAMLIT INTEGRATION
═══════════════════════════════════════════════════════════════════════════════

Add this to your app.py:

---

# At the top, add:
from ml_classifier import InterestClassifier
from ml_inference import InterestPredictor

@st.cache_resource
def load_ml_classifier():
    \"\"\"Load ML model (cached for speed)\"\"\"
    classifier = InterestClassifier.load_model("interest_classifier")
    return InterestPredictor(classifier)

# In main():

    # Add to sidebar:
    with st.sidebar:
        st.divider()
        use_ml = st.checkbox("🤖 Use ML Classifier (experimental)", value=False)
    
    # ... transcription code ...
    
    # When scoring interests:
    if use_ml:
        st.info("Using ML-based interest classifier")
        predictor = load_ml_classifier()
        result = predictor.predict_single(cleaned)
        
        # Display confidence
        conf = result['confidence']
        if conf > 0.7:
            st.success(f"✓ High confidence ({conf:.0%})")
        elif conf > 0.45:
            st.warning(f"~ Medium confidence ({conf:.0%})")
        else:
            st.error(f"⚠ Low confidence ({conf:.0%})")
        
        # Convert to format matching keyword scorer
        interest_scores = {
            p['interest']: p['confidence'] * 100 
            for p in result['all_predictions']
        }
    else:
        interest_scores = score_interests(cleaned)
    
    # ... rest of display code (unchanged) ...

---


═══════════════════════════════════════════════════════════════════════════════
DEPLOYMENT CHECKLIST
═══════════════════════════════════════════════════════════════════════════════

Before going live:

☐ Model file (interest_classifier_*.pkl) copied to deploy folder
☐ requirements_ml.txt added to deploy requirements
☐ Cache settings optimized for your deployment
☐ Error handling for missing model file
☐ Performance tested (should be <100ms per prediction)
☐ Confidence thresholds tuned for your use case
☐ User feedback mechanism for predictions
☐ Monitoring/logging of predictions in production
☐ Documentation for maintainers
☐ A/B test: keyword vs ML vs hybrid

Example error handling:

    try:
        predictor = load_ml_classifier()
        result = predictor.predict_single(cleaned)
    except FileNotFoundError:
        st.error("ML model not found. Using keyword-based scoring.")
        interest_scores = score_interests(cleaned)
    except Exception as e:
        st.error(f"ML prediction error: {e}. Using keyword fallback.")
        interest_scores = score_interests(cleaned)


═══════════════════════════════════════════════════════════════════════════════

Questions? See ML_GUIDE.md for detailed documentation.
"""
