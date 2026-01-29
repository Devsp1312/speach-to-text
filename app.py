# Try to import Streamlit library for web UI
try:
    import streamlit as st
# If import fails, display error message with installation instructions
except Exception:
    print("Missing Python dependencies. Please activate your virtualenv and install requirements:")
    print("pip install -U pip && pip install -r requirements.txt")
    raise

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


# Run main function when script is executed directly
if __name__ == "__main__":
    main()