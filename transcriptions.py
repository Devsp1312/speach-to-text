import os
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import streamlit as st
from faster_whisper import WhisperModel


# Settings
MAX_AUDIO_MB = 25
DEFAULT_MODEL_SIZE = "small"
DEFAULT_COMPUTE_TYPE = "int8"
MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v2"]
COMPUTE_TYPES = ["int8", "float16", "float32"]
SUPPORTED_AUDIO_TYPES = ["mp3", "wav", "m4a", "aac", "flac", "ogg", "mp4"]


def safe_suffix(filename: str) -> str:
    """Extract file suffix safely."""
    suffix = Path(filename).suffix
    if suffix and len(suffix) <= 10:
        return suffix
    return ".audio"


def format_duration(seconds: Optional[float]) -> Optional[str]:
    """Format seconds into MM:SS format."""
    if seconds is None:
        return None
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"


def available_devices() -> list:
    """Get list of available devices (CPU and CUDA if available)."""
    devices = ["cpu"]
    try:
        import ctranslate2

        if ctranslate2.get_cuda_device_count() > 0:
            devices.append("cuda")
    except Exception:
        pass
    return devices


@st.cache_resource
def load_model(model_size: str, device: str, compute_type: str) -> WhisperModel:
    """Load and cache the Whisper model."""
    return WhisperModel(model_size, device=device, compute_type=compute_type)


@st.cache_data(show_spinner=False)
def transcribe_audio_bytes(
    audio_bytes: bytes,
    filename: str,
    model_size: str,
    device: str,
    compute_type: str,
    vad_filter: bool,
    language: str,
) -> Tuple[str, dict]:
    """Transcribe audio bytes to text using Whisper model."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=safe_suffix(filename)) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        model = load_model(model_size, device, compute_type)
        segments, info = model.transcribe(
            tmp_path,
            vad_filter=vad_filter,
            language=language or None,
        )
        transcript = " ".join(seg.text for seg in segments).strip()
        meta = {
            "language": getattr(info, "language", None),
            "language_probability": getattr(info, "language_probability", None),
            "duration": getattr(info, "duration", None),
        }
        return transcript, meta
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def get_audio_bytes(uploaded) -> bytes:
    """Get audio bytes from uploaded file with size validation."""
    if uploaded.size and uploaded.size > MAX_AUDIO_MB * 1024 * 1024:
        st.error(f"File is too large. Please upload an audio file under {MAX_AUDIO_MB} MB.")
        st.stop()
    return uploaded.getvalue()


def render_transcription_sidebar() -> dict:
    """Render transcription settings in sidebar."""
    with st.sidebar:
        st.header("Transcription settings")
        devices = available_devices()
        model_size = st.selectbox("Model size", MODEL_SIZES, index=MODEL_SIZES.index(DEFAULT_MODEL_SIZE))
        device = st.selectbox("Device", devices, index=0)
        compute_type = st.selectbox("Compute type", COMPUTE_TYPES, index=COMPUTE_TYPES.index(DEFAULT_COMPUTE_TYPE))
        vad_filter = st.checkbox("Enable VAD", value=True)
        language = st.text_input("Language (optional)", value="", placeholder="e.g., en, es")
    
    return {
        "model_size": model_size,
        "device": device,
        "compute_type": compute_type,
        "vad_filter": vad_filter,
        "language": language.strip(),
    }
