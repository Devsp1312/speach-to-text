# Try to import Streamlit library for web UI
try:
    import streamlit as st
# If import fails, display error message with installation instructions
except Exception:
    print("Missing Python dependencies. Please activate your virtualenv and install requirements:")
    print("pip install -U pip && pip install -r requirements.txt")
    raise

# Import type hints
from typing import Dict

# Import audio transcription functions from transcriptions module
from transcriptions import (
    transcribe_audio_bytes,  # Function to convert audio to text
    get_audio_bytes,  # Function to extract bytes from uploaded file
    render_transcription_sidebar,  # Function to render settings sidebar
    format_duration,  # Function to format duration in MM:SS format
    SUPPORTED_AUDIO_TYPES,  # List of supported audio file types
)
# Import text analysis and interest scoring functions from interests module
from interests import (
    clean_text,  # Function to clean and normalize text
    score_interests,  # Function to score text against interest categories
    get_top_interests,  # Function to get top N interest categories
    format_interest_table,  # Function to format scores for display
)
# Import user profiling functions from profiles module
from profiles import (
    create_profile,  # Function to generate anonymous user profile
    format_profile_for_display,  # Function to format profile for display
)


# Demo profiles with pre-made interest scores
DEMO_PROFILES = {
    "🤖 Tech Enthusiast": {
        "Tech/Engineering": 45.0,
        "Career/Jobs": 25.0,
        "Academics/School": 15.0,
        "Entertainment/Gaming": 10.0,
        "Food": 5.0,
    },
    "🎉 Social Butterfly": {
        "Social/People": 50.0,
        "Food": 20.0,
        "Entertainment/Gaming": 15.0,
        "Sports/Fitness": 10.0,
        "Career/Jobs": 5.0,
    },
    "💪 Fitness Focused": {
        "Sports/Fitness": 50.0,
        "Food": 20.0,
        "Career/Jobs": 15.0,
        "Social/People": 10.0,
        "Academics/School": 5.0,
    },
    "📚 Academics First": {
        "Academics/School": 45.0,
        "Career/Jobs": 25.0,
        "Tech/Engineering": 15.0,
        "Social/People": 10.0,
        "Entertainment/Gaming": 5.0,
    },
    "🎮 Gamer": {
        "Entertainment/Gaming": 50.0,
        "Tech/Engineering": 20.0,
        "Social/People": 15.0,
        "Food": 10.0,
        "Sports/Fitness": 5.0,
    },
    "⚖️ Balanced": {
        "Social/People": 22.0,
        "Tech/Engineering": 20.0,
        "Career/Jobs": 18.0,
        "Sports/Fitness": 18.0,
        "Entertainment/Gaming": 12.0,
        "Food": 10.0,
    },
}


def render_demo_mode() -> None:
    """Render interactive demo mode for testing profiles without audio."""
    st.markdown('<div class="section-title">🎮 Interactive Profile Demo</div>', unsafe_allow_html=True)
    st.write("Try preset profiles or customize your own interests below")
    st.divider()
    
    # Category emojis for visual clarity
    category_emojis = {
        "Tech/Engineering": "💻",
        "Academics/School": "📚",
        "Career/Jobs": "💼",
        "Sports/Fitness": "💪",
        "Food": "🍔",
        "Social/People": "👥",
        "Entertainment/Gaming": "🎮",
    }
    
    # Preset profiles selection
    st.markdown("**Step 1: Choose a Preset Profile (or skip to customize)**")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    preset_options = list(DEMO_PROFILES.keys())
    with col1:
        if st.button("📗 Load Tech Enthusiast", use_container_width=True):
            st.session_state.preset = preset_options[0]
    with col2:
        if st.button("🎉 Load Social Butterfly", use_container_width=True):
            st.session_state.preset = preset_options[1]
    with col3:
        if st.button("💪 Load Fitness Focused", use_container_width=True):
            st.session_state.preset = preset_options[2]
    
    # Get initial preset
    if "preset" not in st.session_state:
        st.session_state.preset = preset_options[0]
    
    preset_scores = DEMO_PROFILES[st.session_state.preset]
    
    # Initialize session state for custom scores
    if "custom_scores" not in st.session_state:
        st.session_state.custom_scores = preset_scores.copy()
    
    st.divider()
    
    # Custom interests sliders
    st.markdown("**Step 2: Adjust Your Interests (Drag sliders)**")
    st.write("*How interested are you in each category? (0 = not interested, 100 = very interested)*")
    
    # Display sliders in a single column with clear labels
    custom_scores = {}
    for category in preset_scores.keys():
        emoji = category_emojis.get(category, "")
        value = st.session_state.custom_scores.get(category, preset_scores[category])
        custom_scores[category] = st.slider(
            f"{emoji} {category}",
            min_value=0.0,
            max_value=100.0,
            value=value,
            step=5.0,
        )
    
    # Update session state
    st.session_state.custom_scores = custom_scores
    
    # Use custom scores for profile generation
    active_scores = custom_scores
    
    # Normalize scores to percentages
    total = sum(active_scores.values())
    if total > 0:
        normalized_scores = {k: (v / total * 100) for k, v in active_scores.items()}
    else:
        normalized_scores = active_scores
    
    st.divider()
    
    # Display results
    st.markdown("**Your Interest Breakdown:**")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Score Distribution:**")
        import pandas as pd
        df = pd.DataFrame(list(normalized_scores.items()), columns=["Category", "Score"])
        df = df[df["Score"] > 0].sort_values("Score", ascending=False)
        df["Category"] = df["Category"].apply(lambda x: category_emojis.get(x, "") + " " + x)
        st.bar_chart(df.set_index("Category"))
    
    with col2:
        st.markdown("**Percentages:**")
        score_df = []
        for cat, score in sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True):
            if score > 0:
                emoji = category_emojis.get(cat, "")
                score_df.append({"Interest": f"{emoji} {cat}", "Percentage": f"{score:.0f}%"})
        if score_df:
            st.table(score_df)
    
    st.divider()
    
    # Generate and display profile
    st.markdown("**Step 3: Your Generated Profile**")
    st.write("*Based on your interest scores*")
    
    profile = create_profile(normalized_scores)
    profile_display = format_profile_for_display(profile)
    
    # Display profile characteristics in columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Social Style", profile_display["Social Style"])
    with col2:
        st.metric("Activity Preference", profile_display["Activity Preference"])
    
    # Display interests
    st.markdown("**Core Interests:**")
    st.write(profile_display["Core Interests"])
    if profile_display["Secondary Interests"] != "None":
        st.markdown("**Secondary Interests:**")
        st.write(profile_display["Secondary Interests"])
    
    # Display reasoning
    st.markdown("**Profile Reasoning:**")
    st.info(profile_display["Reasoning"])
    
    # Display suggestions
    st.markdown("**Personalized Suggestions:**")
    for i, suggestion in enumerate(profile_display["Suggestions"], 1):
        st.write(f"{i}. {suggestion}")


def display_profile_section(interest_scores: Dict[str, float]) -> None:
    """Display the profile section for regular (non-demo) mode."""
    # Generate and display anonymous user profile
    if interest_scores:
        st.divider()
        st.markdown('<div class="section-title">📊 Anonymous User Profile</div>', unsafe_allow_html=True)
        st.write("*No personal identity information is stored*")
        
        # Create profile from interest scores
        profile = create_profile(interest_scores)
        profile_display = format_profile_for_display(profile)
        
        # Display profile characteristics in columns
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Social Style", profile_display["Social Style"])
        with col2:
            st.metric("Activity Preference", profile_display["Activity Preference"])
        
        # Display core and secondary interests
        st.markdown("**Core Interests:**")
        st.write(profile_display["Core Interests"])
        if profile_display["Secondary Interests"] != "None":
            st.markdown("**Secondary Interests:**")
            st.write(profile_display["Secondary Interests"])
        
        # Display reasoning
        st.markdown("**Profile Reasoning:**")
        st.info(profile_display["Reasoning"])
        
        # Display personalized suggestions
        st.markdown("**Personalized Suggestions:**")
        for i, suggestion in enumerate(profile_display["Suggestions"], 1):
            st.write(f"{i}. {suggestion}")


# Main application function that runs the Streamlit app
def main() -> None:
    # Configure page title and icon
    st.set_page_config(
        page_title="Audio → Speech-to-Text → Interests",
        page_icon="🎧",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for clean styling
    st.markdown("""
        <style>
        /* Clean header styling */
        .main-header {
            font-size: 2.5em;
            font-weight: 600;
            color: #1F2937;
            margin-bottom: 0.5em;
        }
        /* Subtitle styling */
        .subtitle {
            font-size: 1.1em;
            color: #6B7280;
            margin-bottom: 1.5em;
        }
        /* Section styling */
        .section-title {
            font-size: 1.3em;
            font-weight: 600;
            color: #1F2937;
            margin-top: 1em;
            margin-bottom: 0.5em;
        }
        /* Improve spacing */
        .stDivider {
            margin: 2em 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Display main title
    st.markdown('<div class="main-header">🎧 Audio → Speech-to-Text → Interests</div>', unsafe_allow_html=True)
    # Display description
    st.markdown('<div class="subtitle">Upload audio to transcribe and discover interest categories</div>', unsafe_allow_html=True)

    # Display settings sidebar and get user configuration
    settings = render_transcription_sidebar()
    
    # Add demo mode toggle in sidebar
    with st.sidebar:
        st.divider()
        st.subheader("Demo Mode")
        demo_mode = st.checkbox("🎮 Try Demo Mode (no audio needed)", value=False)

    # Demo mode: interactive profile testing without audio
    if demo_mode:
        render_demo_mode()
        return

    # Create file uploader for audio files
    st.markdown('<div class="section-title">📁 Upload Audio</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload audio", type=SUPPORTED_AUDIO_TYPES, label_visibility="collapsed")
    # If no file uploaded, show message and exit
    if not uploaded:
        st.info("Upload an audio file to start.")
        return

    # Extract and validate audio bytes from the uploaded file
    audio_bytes = get_audio_bytes(uploaded)

    # Show loading spinner while transcribing audio
    with st.spinner("Transcribing..."):
        # Call Whisper model to transcribe audio to text
        transcript, meta = transcribe_audio_bytes(
            audio_bytes=audio_bytes,
            filename=uploaded.name,
            model_size=settings["model_size"],  # Model size (tiny, base, small, medium, large)
            device=settings["device"],  # Device to use (cpu or cuda)
            compute_type=settings["compute_type"],  # Computation precision (int8, float16, float32)
            vad_filter=settings["vad_filter"],  # Enable voice activity detection
            language=settings["language"],  # Language code (optional)
        )

    # If language was detected, display metadata about transcription
    if meta.get("language"):
        lang_prob = meta.get("language_probability")  # Get language detection confidence
        duration = format_duration(meta.get("duration"))  # Format duration as MM:SS
        parts = [f"Language: {meta['language']}"]  # Start with detected language
        # Add confidence percentage if available
        if isinstance(lang_prob, float):
            parts.append(f"Confidence: {lang_prob * 100:.1f}%")
        # Add formatted duration if available
        if duration:
            parts.append(f"Duration: {duration}")
        # Display metadata separated by bullet points
        st.caption(" • ".join(parts))

    # Clean transcribed text (lowercase and remove special characters)
    cleaned = clean_text(transcript)
    # Score the text against interest categories
    interest_scores = score_interests(cleaned)
    # Create collapsible section for raw transcript
    with st.expander("Transcript (raw)", expanded=False):
        # Display transcript text or placeholder if empty
        st.write(transcript if transcript else "(empty)")
        # Add download button if transcript has content
        if transcript:
            st.download_button("Download transcript", transcript, file_name="transcript.txt")

    # Display section header for predicted interests
    st.markdown('<div class="section-title">📊 Predicted Interests</div>', unsafe_allow_html=True)
    # Display all interest scores in table format
    st.table(format_interest_table(interest_scores))

    # Get top 3 interests by score
    top3 = get_top_interests(interest_scores, top_n=3)
    # Display section header for top interests
    st.markdown('<div class="section-title">🏆 Top Tags</div>', unsafe_allow_html=True)
    # Display top 3 interests or message if no matches found
    st.write(top3 if top3 else ["No clear matches — add more keywords to your taxonomy."])

    # Display the profile section
    display_profile_section(interest_scores)


# Run main function when script is executed directly
if __name__ == "__main__":
    main()