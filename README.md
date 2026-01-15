# Speech-to-Text Interest Tagger

Small Streamlit app that transcribes audio and scores it against a keyword
taxonomy of interests.

## Quickstart
1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -U pip`
4. `pip install -r requirements.txt`
5. `streamlit run app.py`

## Customize
- Edit `INTEREST_KEYWORDS` in `app.py` to change categories and keywords.
- Adjust limits and defaults in the "App settings" section of `app.py`.

## Notes
- Larger models are slower on CPU.
- If you see audio decode errors, install ffmpeg for your system.
