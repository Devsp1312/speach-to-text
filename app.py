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
    st.subheader("🎮 Interactive Profile Demo")
    st.write("Adjust interest scores in real-time to see how profiles change instantly!")
    
    # Create two columns: preset profiles and custom sliders
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("**Quick Presets:**")
        selected_preset = st.radio("Choose a profile:", list(DEMO_PROFILES.keys()), label_visibility="collapsed")
        preset_scores = DEMO_PROFILES[selected_preset]
    
    with col2:
        st.markdown("**Custom Interests (Drag to adjust):**")
        
        # Initialize session state for custom scores
        if "custom_scores" not in st.session_state:
            st.session_state.custom_scores = preset_scores.copy()
        
        # Interactive sliders for each interest category
        custom_scores = {}
        for category in preset_scores.keys():
            value = st.session_state.custom_scores.get(category, preset_scores[category])
            custom_scores[category] = st.slider(
                category,
                min_value=0.0,
                max_value=100.0,
                value=value,
                step=5.0,
                label_visibility="collapsed"
            )
        
        # Update session state
        st.session_state.custom_scores = custom_scores
    
    # Use custom scores for profile generation
    active_scores = custom_scores if st.session_state.custom_scores else preset_scores
    
    # Normalize scores to percentages
    total = sum(active_scores.values())
    if total > 0:
        normalized_scores = {k: (v / total * 100) for k, v in active_scores.items()}
    else:
        normalized_scores = active_scores
    
    st.divider()
    
    # Display scores visualization
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Interest Scores:**")
        score_df = []
        for cat, score in sorted(normalized_scores.items(), key=lambda x: x[1], reverse=True):
            if score > 0:
                score_df.append({"Category": cat, "Score (%)": f"{score:.1f}"})
        if score_df:
            st.table(score_df)
    
    with col2:
        st.markdown("**Score Distribution:**")
        # Create a simple bar chart
        import pandas as pd
        df = pd.DataFrame(list(normalized_scores.items()), columns=["Category", "Score"])
        df = df[df["Score"] > 0].sort_values("Score", ascending=False)
        st.bar_chart(df.set_index("Category"))
    
    st.divider()
    
    # Generate and display profile
    st.subheader("📊 Real-Time Profile Preview")
    st.write("*This profile updates instantly as you adjust the sliders above.*")
    
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
        st.subheader("📊 Anonymous User Profile")
        st.write("*This profile resets daily and contains no personal identity information.*")
        
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
    st.set_page_config(page_title="Audio → Speech-to-Text → Interests", page_icon="🎧")
    # Display main title
    st.title("Audio → Speech-to-Text → Interests")
    # Display description of app functionality
    st.write("Upload up to ~5 minutes of audio. The app transcribes it and predicts interest categories.")

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
    uploaded = st.file_uploader("Upload audio", type=SUPPORTED_AUDIO_TYPES)
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
    st.subheader("Predicted Interests")
    # Display all interest scores in table format
    st.table(format_interest_table(interest_scores))

    # Get top 3 interests by score
    top3 = get_top_interests(interest_scores, top_n=3)
    # Display section header for top interests
    st.subheader("Top Tags")
    # Display top 3 interests or message if no matches found
    st.write(top3 if top3 else ["No clear matches — add more keywords to your taxonomy."])

    # Display the profile section
    display_profile_section(interest_scores)


# Run main function when script is executed directly
if __name__ == "__main__":
    main()