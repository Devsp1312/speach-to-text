# Demo Mode - Real-Time Profile Testing

## What is Demo Mode?

Demo Mode lets you see profiles change **instantly in real-time** without needing to upload audio files. Perfect for understanding the profiling system and testing different interest combinations.

## How to Use

### Start the App
```bash
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text"
source venv/bin/activate
streamlit run app.py
```

### Enable Demo Mode
1. In the sidebar, you'll see: **"🎮 Try Demo Mode (no audio needed)"**
2. Check the box to enable
3. The app switches to interactive demo mode instantly

## Features

### 📋 Quick Presets
Choose from 6 pre-built profiles:
- **🤖 Tech Enthusiast** - Heavy on Tech/Engineering & Career
- **🎉 Social Butterfly** - Focused on Social/People & Food
- **💪 Fitness Focused** - Sports/Fitness dominant
- **📚 Academics First** - Study-oriented with career focus
- **🎮 Gamer** - Entertainment/Gaming with tech
- **⚖️ Balanced** - Even mix across all categories

### 🎚️ Interactive Sliders
- Adjust each interest category from 0-100
- Sliders update in real-time
- **Scores automatically normalize to percentages**
- Drag to see instant profile changes

### 📊 Live Visualizations
**Left panel:**
- Interest scores table
- Shows normalized percentages

**Right panel:**
- Bar chart of interest distribution
- Visual comparison of categories

### 📈 Real-Time Profile Updates
As you adjust sliders, the profile section below updates instantly showing:
- **Social Style** - How you prefer social interaction
- **Activity Preference** - Solo, small group, or large group
- **Core Interests** - Your top 3 interests
- **Secondary Interests** - Next tier of interests
- **Reasoning** - Explanation of profile
- **Suggestions** - 3 personalized recommendations

## Example Scenarios

### Scenario 1: Create a Tech Person
1. Select **🤖 Tech Enthusiast** preset
2. Increase **Tech/Engineering** to 60
3. Increase **Career/Jobs** to 30
4. Watch the profile update:
   - Social Style → Introverted or Balanced
   - Activity Preference → Solo or Small Group
   - Suggestions → Coding meetups, side projects

### Scenario 2: Make Them Social
1. Adjust the sliders:
   - **Social/People** → 80
   - **Food** → 15
   - **Others** → keep low
2. Profile changes to:
   - Social Style → Extroverted
   - Activity Preference → Large Group
   - Suggestions → Parties, hangouts, events

### Scenario 3: Balanced Person
1. Select **⚖️ Balanced** preset
2. All categories get ~15-20%
3. Profile shows:
   - Social Style → Balanced
   - Activity Preference → Small Group
   - Suggestions → Mix of activities

### Scenario 4: Athlete
1. Increase **Sports/Fitness** to 70
2. Increase **Food** to 20
3. Keep others low
4. Profile shows:
   - Strong fitness focus
   - Balanced social style
   - Suggestions → Gym class, intramural teams

## Real-Time Changes

**Notice how the profile updates instantly:**
1. ✅ Social Style changes when you adjust social-related categories
2. ✅ Activity Preference changes based on group-size patterns
3. ✅ Suggestions regenerate based on top interests
4. ✅ Reasoning updates to reflect new interest distribution
5. ✅ Bar chart refreshes showing new percentages

## Understanding Profile Changes

### What Makes Someone Extroverted?
High scores in:
- Social/People (most important)
- Food
- Career/Jobs

### What Makes Someone Introverted?
High scores in:
- Tech/Engineering
- Academics/School
- Entertainment/Gaming

### What Determines Activity Preference?
- **Solo:** Tech, Gaming, Academics
- **Small Group:** Balanced mix, Career focus
- **Large Group:** Social/People, Food, Events

## Tips

💡 **Experiment with extremes:**
- Set one category to 100, others to 0
- See how extreme profiles differ
- Mix different profiles together

💡 **Check suggestions:**
- Different social styles get different suggestions
- Same interests = different suggestions based on social style
- Notice how introverts get more solo-friendly options

💡 **Watch the bar chart:**
- Visual representation helps understand percentages
- See how profiles change as you drag sliders
- Easier than reading numbers

💡 **Test realistic combinations:**
- Create profiles that feel like real people
- See if suggestions make sense for that person
- Identify gaps in the suggestion system

## Switching Between Modes

### From Demo to Real Audio
1. Uncheck "🎮 Try Demo Mode"
2. Click "Upload audio" button
3. Upload your file and process normally

### From Real Audio to Demo
1. Check "🎮 Try Demo Mode" in sidebar
2. App switches instantly to demo mode
3. Your uploaded data is not lost

## Common Questions

**Q: Are my changes saved?**
A: No, changes are temporary for the current session. Reload page to reset.

**Q: Can I export the profile?**
A: Not yet - profiles are for visualization only. Future versions could add export.

**Q: Why do scores normalize?**
A: Ensures percentages always add to 100% for consistent profile generation.

**Q: Can I add more presets?**
A: Yes! Edit `DEMO_PROFILES` in `app.py` to add custom presets.

## Next Steps

After exploring demo mode:
1. ✅ Upload real audio to see actual profiles
2. ✅ Compare real profiles with demo profiles
3. ✅ Customize interest keywords if needed
4. ✅ Add more suggestion ideas
5. ✅ Deploy the app to share with others
