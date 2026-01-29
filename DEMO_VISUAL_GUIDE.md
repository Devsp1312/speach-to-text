# Demo Mode - Visual Walkthrough

## 🎬 What You'll See When You Run Demo Mode

### Step 1: App Starts
```
┌─────────────────────────────────────────────────┐
│  Audio → Speech-to-Text → Interests         🎧  │
├─────────────────────────────────────────────────┤
│  Upload up to ~5 minutes of audio...            │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ 🎮 Try Demo Mode (no audio needed)  ✓    │ │  ← CHECK THIS
│  └────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### Step 2: Demo Mode Activates
```
┌──────────────────────────────────────────────────────────┐
│          🎮 Interactive Profile Demo                      │
│  Adjust interest scores in real-time to see how          │
│  profiles change instantly!                               │
└──────────────────────────────────────────────────────────┘

┌────────────────────────┬──────────────────────────────────┐
│   Quick Presets:       │   Custom Interests (Drag to      │
│                        │   adjust):                        │
│  ○ 🤖 Tech Enthusiast │                                   │
│  ○ 🎉 Social Butterfly│   Tech/Engineering ═════════ 45  │
│  ○ 💪 Fitness Focused │   Career/Jobs      ════════ 25   │
│  ○ 📚 Academics First │   Social/People    ======= 15    │
│  ○ 🎮 Gamer           │   Sports/Fitness   ===== 12      │
│  ● ⚖️ Balanced        │   Food             ===== 8       │
│                        │   Academics/School = 2           │
│                        │   Entertainment/Gaming = 1       │
└────────────────────────┴──────────────────────────────────┘

─────────────────────────────────────────────────────────────

┌─────────────────────────────┬──────────────────────────────┐
│ Interest Scores:            │ Score Distribution:          │
│                             │                              │
│ Category        Score (%)   │ ▄▄▄ Tech/Eng         45%    │
│ Tech/Eng        45.0%       │ ▄▄  Career/Jobs      25%    │
│ Career/Jobs     25.0%       │ ▄   Social/People    15%    │
│ Social/People   15.0%       │ ▄   Sports/Fit       12%    │
│ Sports/Fitness  12.0%       │ ▂   Food              8%    │
│ Food             8.0%       │ ▁   Academics         2%    │
│ Academics        2.0%       │ ▁   Entertainment     1%    │
│ Entertainment    1.0%       │                              │
│                             │                              │
└─────────────────────────────┴──────────────────────────────┘

─────────────────────────────────────────────────────────────

        📊 Real-Time Profile Preview

*This profile updates instantly as you adjust the sliders above.*

┌──────────────────────────┬─────────────────────────┐
│  Social Style: Balanced  │  Activity Pref: Small   │
│                          │  group activities       │
└──────────────────────────┴─────────────────────────┘

Core Interests:
Tech/Engineering, Career/Jobs, Social/People

Secondary Interests:
Sports/Fitness, Food

Profile Reasoning:
Based on your transcribed content, your profile centers on 
Tech/Engineering, Career/Jobs, Social/People. With 
'Tech/Engineering' as your strongest interest (45.0%), your 
social style suggests a preference for balanced engagement. 
You appear to thrive with small group activities, allowing 
for both focused individual pursuits and meaningful 
interactions when you choose them.

Personalized Suggestions:
1. Start a small side project using a language you've wanted 
   to learn
2. Attend a career fair or industry networking event
3. Plan a hangout with friends you haven't seen recently
```

---

## 🎮 Real-Time Changes Demo

### When You Select Different Preset:
```
Before: Selecting 🎉 Social Butterfly
┌─────────────────────┐
│ Social Style        │
│ Balanced            │  ← Was this
│ Activity: Small     │
│ Group               │
└─────────────────────┘

After: Profile updates instantly!
┌─────────────────────┐
│ Social Style        │
│ Extroverted         │  ← Changed!
│ Activity: Large     │
│ Group               │
└─────────────────────┘

Suggestions also update:
"Plan a hangout with friends you haven't seen recently" → 
  ↓
"Attend a social event or party happening on campus"
```

### When You Drag Sliders:
```
Dragging Tech/Engineering slider from 45 to 80:

At 45%:
• Social Style: Balanced
• Suggestions include networking

At 60%:
• Social Style: Introverted (shifting)
• Suggestions shift toward coding

At 80%:
• Social Style: Introverted (settled)
• Suggestions: Solo-focused tech activities

ALL UPDATES HAPPEN INSTANTLY! ⚡
```

---

## 📊 What Changes in Real-Time

### As you adjust sliders, these update instantly:

```
✓ Interest Scores table (new percentages)
✓ Bar chart (heights change)
✓ Social Style metric (text changes)
✓ Activity Preference metric (text changes)
✓ Core Interests list (reorders)
✓ Secondary Interests list (changes)
✓ Profile Reasoning (rewrites)
✓ Personalized Suggestions (all 3 regenerate)
```

**Everything updates without page refresh!** 🚀

---

## 🎯 Experiment Scenarios

### Scenario: Make Tech Person More Social
```
Initial State (🤖 Tech Enthusiast):
┌─────────────────────────────────────────────────┐
│ Social Style: Introverted                       │
│ Activity: Solo activities                       │
│ Top Interests: Tech, Career, Academics          │
│ Suggestions:                                    │
│ • Attend a coding meetup or hackathon           │
│ • Start a small side project...                 │
│ • Join an online tech community...              │
└─────────────────────────────────────────────────┘

You drag sliders:
• Social/People: 10 → 50
• Tech/Engineering: 45 → 30

┌─────────────────────────────────────────────────┐
│ Social Style: Balanced (changed!)               │
│ Activity: Small group activities (changed!)     │
│ Top Interests: Social/People, Tech, Career      │
│ Suggestions (all updated!):                     │
│ • Plan a hangout with friends...                │
│ • Join an online tech community...              │
│ • Attend a career fair or industry event...     │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Demo Mode Flow

```
┌──────────────────────────┐
│ Select Preset or         │
│ Adjust Custom Sliders    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Scores normalize to      │
│ percentages (instant)    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ create_profile() runs    │
│ (very fast <50ms)        │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ All UI elements update   │
│ instantly (real-time)    │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Profile displayed with   │
│ all sections updated     │
└──────────────────────────┘
```

---

## 💡 Tips for Using Demo Mode

### To See Big Changes:
1. Select 🤖 Tech Enthusiast preset
2. Drag Social/People to max (100)
3. Notice social style changed to Extroverted
4. Suggestions became very social-focused

### To See Subtle Changes:
1. Select ⚖️ Balanced preset
2. Slowly drag one slider from 15 → 40
3. Watch how profile gradually shifts
4. Social style stays balanced, but activity preference might change

### To Test All Combinations:
1. Set all sliders to 0
2. Set only one to 50
3. See profile for single-interest person
4. Then mix interests together

---

## 🎨 UI Elements You'll Interact With

```
SIDEBAR (Left):
├─ Model size dropdown
├─ Device selector
├─ Compute type
├─ VAD checkbox
├─ Language input
├─ DIVIDER
└─ Demo Mode Toggle ← CLICK THIS

MAIN AREA (When Demo Enabled):
├─ Title: "🎮 Interactive Profile Demo"
├─ Two columns:
│  ├─ Left: Quick Presets (radio buttons)
│  └─ Right: Custom Sliders (7 sliders)
├─ DIVIDER
├─ Score visualization:
│  ├─ Left: Table
│  └─ Right: Bar chart
├─ DIVIDER
├─ Profile section:
│  ├─ Metrics (2 columns)
│  ├─ Core interests
│  ├─ Secondary interests
│  ├─ Reasoning (info box)
│  └─ Suggestions (numbered list)
```

---

## ⚡ Performance Expectations

```
Action               Response Time
─────────────────────────────────
Toggle Demo Mode     Instant (no load)
Select Preset        <100ms (very fast)
Drag Slider          <50ms (real-time)
Profile Update       <50ms (immediate)
Page Load            Instant (no loading)
```

**You'll see changes before you finish moving the mouse!** ✨

---

## 🎓 What You Learn from Demo Mode

1. **Interest Combinations** → See how different mixes create different profiles
2. **Social Style Logic** → Understand which interests create which styles
3. **Suggestions Engine** → See why certain people get certain suggestions
4. **Profile Generation** → Watch the algorithm work in real-time
5. **System Design** → Get insight into how the profiling works

---

## 🚀 Ready? Here's the Command

```bash
cd "/Users/devpatel/VS_Code/Capstone Project/speach to text"
source venv/bin/activate
streamlit run app.py
```

Then check "🎮 Try Demo Mode" in the sidebar!

**You're going to love watching those profiles change in real-time!** 🎉
