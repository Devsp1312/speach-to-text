# Quick Start - Run and Test Demo Mode

## 🚀 Start the App (One Command)

```bash
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text"
source venv/bin/activate
streamlit run app.py
```

The app opens at `http://localhost:8501`

---

## 🎮 Using Demo Mode (No Audio Upload Needed!)

### Step 1: Enable Demo Mode
1. Look at the left sidebar
2. Find section: **"Demo Mode"**
3. Check the box: **"🎮 Try Demo Mode (no audio needed)"**
4. The app instantly switches to interactive demo mode

### Step 2: See Profiles Change in Real-Time

#### Option A: Use Quick Presets
- **Left panel:** Click radio buttons to select presets:
  - 🤖 Tech Enthusiast
  - 🎉 Social Butterfly
  - 💪 Fitness Focused
  - 📚 Academics First
  - 🎮 Gamer
  - ⚖️ Balanced
- Profile updates instantly when you select a preset

#### Option B: Custom Sliders
- **Right panel:** Drag sliders to adjust interest scores
- Each slider = one interest category (0-100)
- Scores automatically normalize to percentages
- **Profile updates in real-time** as you drag!

### Step 3: Watch the Live Updates

As you adjust sliders, you'll see:

✅ **Top:** Interest Scores table + Bar chart  
✅ **Middle:** Social Style & Activity Preference metrics  
✅ **Bottom:** Core interests, reasoning, and personalized suggestions  

**All updating instantly as you move the sliders!**

---

## 📊 What You'll See

### Profile Section Updates These Elements in Real-Time:

| Component | What It Shows |
|-----------|---------------|
| Social Style | Introverted / Balanced / Extroverted |
| Activity Preference | Solo / Small Group / Large Group |
| Core Interests | Top 3 interest categories |
| Secondary Interests | Next tier of interests |
| Reasoning | Explanation of the profile |
| Suggestions | 3 personalized activity ideas |

---

## 🎯 Try These Experiments

### Experiment 1: Tech Person
1. Select **🤖 Tech Enthusiast** preset
2. Notice: Introverted, Solo activities
3. Drag **Tech/Engineering** slider to 80
4. Watch profile shift: More introverted, more solo focus

### Experiment 2: Social Butterfly
1. Select **🎉 Social Butterfly** preset
2. Notice: Extroverted, Large group activities
3. Drag **Social/People** to max
4. Suggestions become party/event focused

### Experiment 3: Create Your Own Profile
1. Set all sliders to 0
2. Gradually increase:
   - **Sports/Fitness**: 40
   - **Food**: 30
   - **Social/People**: 20
   - **Tech/Engineering**: 10
3. See the profile emerge in real-time

### Experiment 4: Test Extremes
1. Set **Tech/Engineering** to 100, others to 0
2. Watch the profile shift dramatically
3. Then drag it back down gradually
4. Notice how suggestions and style change smoothly

---

## 💡 What Makes Profiles Interesting

**The real-time updates show:**
- ✅ How different interest combinations create different profiles
- ✅ Why social categories influence social style
- ✅ How activity-type categories affect group preferences
- ✅ Why suggestions change based on the full profile, not just top interests

---

## 🔄 Switch Back to Audio Mode

1. Uncheck "🎮 Try Demo Mode" in sidebar
2. Upload audio file
3. Wait for transcription
4. See your real profile generated from actual speech!

---

## 📁 Supporting Files

- **[DEMO_MODE.md](DEMO_MODE.md)** - Detailed demo mode guide
- **[TESTING.md](TESTING.md)** - Full testing procedures
- **[README.md](README.md)** - App overview and features

---

## ⚡ Quick Command Reference

```bash
# Start app
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text" && source venv/bin/activate && streamlit run app.py

# Test profiles module standalone
python profiles.py

# Test interest scoring
python -c "from interests import score_interests, clean_text; print(score_interests(clean_text('I love coding')))"

# Check Python syntax
python -m py_compile app.py profiles.py interests.py
```

---

## ✨ Features Enabled

✅ **Audio Transcription** - Upload audio and get transcript  
✅ **Interest Scoring** - Analyzes content against 7 categories  
✅ **Profile Generation** - Creates anonymous user profile  
✅ **Real-Time Demo Mode** - See profiles update as you adjust sliders  
✅ **Preset Profiles** - Quick examples to understand the system  
✅ **Live Visualizations** - Charts and metrics update instantly  

---

## 🎓 What You'll Learn

By using demo mode, you'll understand:
1. How interest scores translate to social styles
2. Why certain categories cluster together
3. How the profiling engine works
4. What factors influence suggestions
5. How different people create different profiles

---

**Ready? Run `streamlit run app.py` and check "Try Demo Mode" to get started!** 🎉
