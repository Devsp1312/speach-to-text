try:
    import streamlit as st
except Exception:
    print("Missing Python dependencies. Please activate your virtualenv and install requirements:")
    print("pip install -U pip && pip install -r requirements.txt")
    raise

from transcriptions import (
    transcribe_audio_bytes,
    get_audio_bytes,
    render_transcription_sidebar,
    format_duration,
    SUPPORTED_AUDIO_TYPES,
)
from interests import (
    clean_text,
    score_interests,
    get_top_interests,
    format_interest_table,
)


def main() -> None:
    st.set_page_config(page_title="Audio → Speech-to-Text → Interests", page_icon="🎧")
    st.title("Audio → Speech-to-Text → Interests")
    st.write("Upload up to ~5 minutes of audio. The app transcribes it and predicts interest categories.")

    settings = render_transcription_sidebar()

    uploaded = st.file_uploader("Upload audio", type=SUPPORTED_AUDIO_TYPES)
    if not uploaded:
        st.info("Upload an audio file to start.")
        return

    audio_bytes = get_audio_bytes(uploaded)
    st.audio(audio_bytes)

    with st.spinner("Transcribing..."):
        transcript, meta = transcribe_audio_bytes(
            audio_bytes=audio_bytes,
            filename=uploaded.name,
            model_size=settings["model_size"],
            device=settings["device"],
            compute_type=settings["compute_type"],
            vad_filter=settings["vad_filter"],
            language=settings["language"],
        )

    if meta.get("language"):
        lang_prob = meta.get("language_probability")
        duration = format_duration(meta.get("duration"))
        parts = [f"Language: {meta['language']}"]
        if isinstance(lang_prob, float):
            parts.append(f"Confidence: {lang_prob * 100:.1f}%")
        if duration:
            parts.append(f"Duration: {duration}")
        st.caption(" • ".join(parts))

    cleaned = clean_text(transcript)
    interest_scores = score_interests(cleaned)

    with st.expander("Transcript (raw)", expanded=False):
        st.write(transcript if transcript else "(empty)")
        if transcript:
            st.download_button("Download transcript", transcript, file_name="transcript.txt")

    st.subheader("Predicted Interests")
    st.table(format_interest_table(interest_scores))

    top3 = get_top_interests(interest_scores, top_n=3)
    st.subheader("Top Tags")
    st.write(top3 if top3 else ["No clear matches — add more keywords to your taxonomy."])


if __name__ == "__main__":
    main()