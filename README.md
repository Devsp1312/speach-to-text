# Speech-to-Text Interest Tagger

Small Streamlit app that transcribes audio and scores it against a keyword
taxonomy of interests. Generates anonymous user profiles with real-time updates.

## Quickstart
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -U pip`
4. `pip install -r requirements.txt`
5. `streamlit run app.py`

## Features

### 🎙️ Audio Transcription
- Upload audio files (MP3, WAV, M4A, FLAC, OGG, MP4)
- Powered by OpenAI's Whisper model
- Configurable model size, device (CPU/GPU), and language

### 🏷️ Interest Scoring
- Analyzes transcribed text against 7 interest categories:
  - Tech/Engineering
  - Academics/School
  - Career/Jobs
  - Sports/Fitness
  - Food
  - Social/People
  - Entertainment/Gaming

### 📊 Anonymous User Profiles
- Generates profiles from interest scores
- Determines social style (Introverted/Balanced/Extroverted)
- Identifies activity preferences (Solo/Small Group/Large Group)
- Provides personalized suggestions
- Profiles reset daily with no personal identity stored

### 🎮 Demo Mode (NEW!)
- **Try interactive profiles without uploading audio**
- Drag sliders to adjust interest scores in real-time
- See profile update instantly as you change values
- Choose preset profiles to quickly test different scenarios
- Perfect for understanding how the profiling system works

## Usage

### Option 1: Upload Audio
1. Run `streamlit run app.py`
2. Upload an audio file (30 seconds to 5 minutes)
3. View transcription, interest scores, and profile

### Option 2: Demo Mode (No Audio Needed!)
1. Run `streamlit run app.py`
2. Check "🎮 Try Demo Mode" in sidebar
3. Adjust sliders to see profiles change in real-time
4. Try different presets: Tech Enthusiast, Social Butterfly, Fitness Focused, etc.

## Customize

### Edit Interest Categories
- Edit `WEIGHTED_KEYWORDS` in `interests.py` to change categories and keywords
- Adjust weights for more/less emphasis on specific keywords

### Modify Suggestions
- Edit `SUGGESTION_TEMPLATES` in `profiles.py` to customize suggestions
- Add new suggestion categories in `DEMO_PROFILES` in `app.py`

### Adjust Settings
- Model size: tiny, base, small, medium, large (larger = more accurate but slower)
- Device: CPU or CUDA (GPU)
- Compute type: int8, float16, float32 (lower precision = faster)

## Notes
- Larger models are slower on CPU
- If you see audio decode errors, install ffmpeg: `brew install ffmpeg`
- First run downloads the Whisper model (~1-3 GB)
- Use "tiny" or "base" model for quick testing
