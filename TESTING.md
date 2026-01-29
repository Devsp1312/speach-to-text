# How to Run and Test the Speech-to-Text Interest Profiler

## Prerequisites

Make sure you have the virtual environment set up and dependencies installed.

```bash
# Navigate to project directory
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text"

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies (if needed)
pip install -U pip
pip install -r requirements.txt
```

## Running the Application

### Start the Streamlit App
```bash
streamlit run app.py
```

This will:
- Start a local web server (typically at `http://localhost:8501`)
- Open the app in your browser automatically
- Display the interface with audio upload and settings

## Testing the App

### Option 1: Quick Test with Sample Audio File

1. **Prepare a test audio file:**
   - Use any audio file you have (MP3, WAV, M4A, FLAC, OGG, or MP4)
   - Recommended: 30 seconds to 5 minutes
   - Content: Talk about your interests, hobbies, or coursework

2. **Upload in the app:**
   - Click "Upload audio" button
   - Select your audio file
   - Adjust settings in sidebar if desired (model size, device, language)
   - Wait for transcription

3. **View results:**
   - Raw transcript in collapsible section
   - Interest scores table
   - Top 3 tags
   - **Anonymous User Profile section** (new!)
     - Social Style
     - Activity Preference
     - Core/Secondary Interests
     - Profile Reasoning
     - 3 Personalized Suggestions

### Option 2: Test Profiling Module Directly

Run the profiling module standalone:

```bash
python profiles.py
```

This runs built-in test examples showing:
- Profile generation from sample interest scores
- Social style determination
- Activity preference calculation
- Suggestion generation

Output will show:
```
============================================================
ANONYMOUS USER PROFILE
============================================================

Core Interests: Tech/Engineering, Career/Jobs, Social/People
Secondary Interests: Sports/Fitness, Food
...
```

### Option 3: Test Individual Components

#### Test Interest Scoring

```bash
python -c "
from interests import score_interests, clean_text

text = 'I love coding in Python and debugging machine learning models'
cleaned = clean_text(text)
scores = score_interests(cleaned)
print('Interest Scores:')
for category, score in sorted(scores.items(), key=lambda x: x[1], reverse=True):
    print(f'  {category}: {score:.1f}%')
"
```

#### Test Profile Generation

```bash
python -c "
from profiles import create_profile

scores = {
    'Tech/Engineering': 45.0,
    'Career/Jobs': 30.0,
    'Social/People': 15.0,
    'Sports/Fitness': 10.0,
}

profile = create_profile(scores)
print('Profile Summary:')
print(f'Social Style: {profile.social_style}')
print(f'Activity Preference: {profile.activity_preference}')
print(f'Suggestions:')
for i, s in enumerate(profile.suggestions, 1):
    print(f'  {i}. {s}')
"
```

## Testing Different Scenarios

### Test 1: Technical Person
**What to say in audio:**
"I'm working on a Python project using machine learning. Just finished debugging some neural networks. Love coding and building stuff. Been learning Docker for deployment."

**Expected profile:**
- Core Interests: Tech/Engineering
- Social Style: Introverted or Balanced
- Suggestions: Coding meetup, side project, tech community

### Test 2: Social/Extroverted Person
**What to say in audio:**
"Going to a party this weekend with friends. Love meeting new people and going out. Just got invited to a networking event for career stuff. Always up for hangouts and events."

**Expected profile:**
- Core Interests: Social/People, Career/Jobs
- Social Style: Extroverted
- Suggestions: Networking, hangouts, events

### Test 3: Fitness Enthusiast
**What to say in audio:**
"Hit a new personal record at the gym today. Been training consistently and eating healthy. Thinking about joining an intramural basketball team. Protein and gains are my thing."

**Expected profile:**
- Core Interests: Sports/Fitness
- Social Style: Balanced
- Suggestions: New fitness class, sports team, workout buddy

### Test 4: Balanced Student
**What to say in audio:**
"Got an exam coming up so I've been studying. Also went to the gym this morning. Planning to grab dinner with friends later and watch a movie. Have an interview coming up too."

**Expected profile:**
- Core Interests: Multiple categories
- Social Style: Balanced
- Activity Preference: Small group activities
- Suggestions: Mix of different activities

## Troubleshooting

### Issue: Model doesn't download/runs slowly
**Solution:**
- First run downloads the Whisper model (~1-3 GB depending on size)
- Use "tiny" or "base" model for testing (faster)
- On CPU, processing takes longer - use GPU if available

### Issue: Audio decode errors
**Solution:**
```bash
# Install ffmpeg for audio handling
brew install ffmpeg  # macOS
# or
sudo apt-get install ffmpeg  # Linux
```

### Issue: Virtual environment not found
**Solution:**
```bash
# Create new venv if missing
python3 -m venv venv
source venv/bin/activate
pip install -U pip
pip install -r requirements.txt
```

### Issue: Streamlit won't start
**Solution:**
```bash
# Check dependencies
pip list | grep streamlit

# Reinstall if needed
pip install streamlit>=1.30 faster-whisper>=1.0
```

## Monitoring Test Results

### Check transcript accuracy:
- Look at the raw transcript (expand "Transcript (raw)" section)
- Verify it captures your speech correctly

### Verify interest scoring:
- Check "Predicted Interests" table
- Your main topics should rank highest

### Validate profile generation:
- Social Style should match your described social behavior
- Suggestions should be relevant and actionable
- Reasoning should logically connect interests to profile

## Sample Test Command

```bash
# Full workflow test
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text"
source venv/bin/activate
streamlit run app.py
```

Then:
1. Upload audio file
2. Wait for transcription
3. Review all output sections
4. Check if profile matches your actual interests/style
5. Verify suggestions are reasonable for a university student

## Next Steps

After testing, you can:
- ✅ Deploy to a public server (Streamlit Cloud, Heroku, etc.)
- ✅ Add more interest categories in `interests.py`
- ✅ Customize suggestions in `profiles.py`
- ✅ Add persistent storage for profile history (with privacy safeguards)
- ✅ Create a dashboard showing trends across multiple uploads
