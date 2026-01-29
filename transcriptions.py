# Import modules for file handling
import os
import tempfile
# Import Path class for file path operations
from pathlib import Path
# Import type hints for better code documentation
from typing import Optional, Tuple

# Import Streamlit for web UI framework
import streamlit as st
# Import Whisper model from faster-whisper library for speech-to-text
from faster_whisper import WhisperModel


# ===== CONFIGURATION CONSTANTS =====
# Maximum audio file size in MB
MAX_AUDIO_MB = 25
# Default Whisper model size to use
DEFAULT_MODEL_SIZE = "small"
# Default computation type (precision level)
DEFAULT_COMPUTE_TYPE = "int8"
# Available Whisper model sizes (larger = more accurate but slower)
MODEL_SIZES = ["tiny", "base", "small", "medium", "large-v2"]
# Available computation types (lower precision = faster but less accurate)
COMPUTE_TYPES = ["int8", "float16", "float32"]
# Supported audio file formats
SUPPORTED_AUDIO_TYPES = ["mp3", "wav", "m4a", "aac", "flac", "ogg", "mp4"]


# Function to safely extract file extension from filename
def safe_suffix(filename: str) -> str:
    """Extract file suffix safely."""
    # Get file extension using Path
    suffix = Path(filename).suffix
    # Return extension if valid (≤10 chars), otherwise return generic audio extension
    if suffix and len(suffix) <= 10:
        return suffix
    return ".audio"


# Function to convert seconds to MM:SS format
def format_duration(seconds: Optional[float]) -> Optional[str]:
    """Format seconds into MM:SS format."""
    # Return None if no duration provided
    if seconds is None:
        return None
    # Calculate minutes by dividing by 60
    minutes = int(seconds // 60)
    # Calculate remaining seconds using modulo
    secs = int(seconds % 60)
    # Return formatted string with zero-padded seconds
    return f"{minutes}:{secs:02d}"


# Function to get available computing devices
def available_devices() -> list:
    """Get list of available devices (CPU and CUDA if available)."""
    # Start with CPU as always available option
    devices = ["cpu"]
    # Try to check for CUDA (GPU) support
    try:
        import ctranslate2

        # Check if CUDA devices are available
        if ctranslate2.get_cuda_device_count() > 0:
            devices.append("cuda")  # Add CUDA option if GPU found
    except Exception:
        pass  # If CUDA not available, just use CPU
    return devices


# Decorator to cache the Whisper model in memory (so it's loaded only once)
@st.cache_resource
def load_model(model_size: str, device: str, compute_type: str) -> WhisperModel:
    """Load and cache the Whisper model."""
    # Initialize and return Whisper model with specified settings
    return WhisperModel(model_size, device=device, compute_type=compute_type)


# Decorator to cache transcription results (so same audio doesn't get transcribed twice)
@st.cache_data(show_spinner=False)
def transcribe_audio_bytes(
    audio_bytes: bytes,  # Audio data as bytes
    filename: str,  # Original filename
    model_size: str,  # Model size to use
    device: str,  # Device (cpu or cuda)
    compute_type: str,  # Computation precision
    vad_filter: bool,  # Voice Activity Detection filter
    language: str,  # Language code (optional)
) -> Tuple[str, dict]:
    """Transcribe audio bytes to text using Whisper model."""
    # Create temporary file to store audio bytes (Whisper needs file path)
    with tempfile.NamedTemporaryFile(delete=False, suffix=safe_suffix(filename)) as tmp:
        tmp.write(audio_bytes)  # Write audio bytes to temp file
        tmp_path = tmp.name  # Get temp file path

    # Try-finally to ensure temp file is cleaned up
    try:
        # Load the Whisper model
        model = load_model(model_size, device, compute_type)
        # Run transcription on the audio file
        segments, info = model.transcribe(
            tmp_path,
            vad_filter=vad_filter,  # Enable/disable voice detection
            language=language or None,  # Set language (None for auto-detect)
        )
        # Join all transcribed segments into single string
        transcript = " ".join(seg.text for seg in segments).strip()
        # Extract metadata about transcription
        meta = {
            "language": getattr(info, "language", None),  # Detected language
            "language_probability": getattr(info, "language_probability", None),  # Detection confidence
            "duration": getattr(info, "duration", None),  # Audio duration in seconds
        }
        # Return transcript text and metadata
        return transcript, meta
    finally:
        # Always try to clean up temp file even if error occurs
        try:
            os.remove(tmp_path)
        except OSError:
            pass  # Ignore errors if file already deleted


# Function to extract and validate audio bytes from uploaded file
def get_audio_bytes(uploaded) -> bytes:
    """Get audio bytes from uploaded file with size validation."""
    # Check if file size exceeds maximum allowed
    if uploaded.size and uploaded.size > MAX_AUDIO_MB * 1024 * 1024:
        # Show error message if file too large
        st.error(f"File is too large. Please upload an audio file under {MAX_AUDIO_MB} MB.")
        st.stop()  # Stop execution
    # Return file contents as bytes
    return uploaded.getvalue()


# Function to create and render sidebar settings for transcription
def render_transcription_sidebar() -> dict:
    """Render transcription settings in sidebar."""
    # Create sidebar section
    with st.sidebar:
        # Display sidebar header
        st.header("Transcription settings")
        # Get list of available devices (CPU/CUDA)
        devices = available_devices()
        # Dropdown to select model size
        model_size = st.selectbox("Model size", MODEL_SIZES, index=MODEL_SIZES.index(DEFAULT_MODEL_SIZE))
        # Dropdown to select device (CPU or GPU)
        device = st.selectbox("Device", devices, index=0)
        # Dropdown to select computation type (precision level)
        compute_type = st.selectbox("Compute type", COMPUTE_TYPES, index=COMPUTE_TYPES.index(DEFAULT_COMPUTE_TYPE))
        # Checkbox to enable/disable Voice Activity Detection
        vad_filter = st.checkbox("Enable VAD", value=True)
        # Text input for optional language code (e.g., "en" for English)
        language = st.text_input("Language (optional)", value="", placeholder="e.g., en, es")
    
    # Return dictionary with all selected settings
    return {
        "model_size": model_size,
        "device": device,
        "compute_type": compute_type,
        "vad_filter": vad_filter,
        "language": language.strip(),  # Remove leading/trailing whitespace
    }
