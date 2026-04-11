# NEUROLEARN ASSIST

AI education assistant for blind, deaf, and general learners.

## Stack
- Frontend: React + TypeScript + Tailwind
- Backend: FastAPI + Gemini + FAISS
- OCR: pdfplumber + pytesseract + Pillow
- STT: Hugging Face `facebook/wav2vec2-base-960h`
- TTS: ElevenLabs (Rachel voice)
- Voice Conversion: RVC HFV2 (Hugging Face model + optional external RVC infer script)
- Braille: Serial output to Arduino

## Project Structure
- backend/
- frontend/
- hardware/arduino_braille_interface/

## Backend Setup
1. Create Python env and install dependencies:
   - `pip install -r backend/requirements.txt`
2. Install Tesseract OCR and FFmpeg and ensure both are available on PATH.
3. Copy `backend/.env.example` to `backend/.env` and configure values.
4. Optional for full RVC runtime:
   - Set `RVC_MODEL_REPO` to your Hugging Face RVC model repo.
   - Set `RVC_INFER_SCRIPT` to your local RVC inference entry script.
5. Run API:
   - `uvicorn main:app --reload --app-dir backend`

## Backend Environment Variables
- `GEMINI_API_KEY`
- `TESSERACT_CMD` (optional)
- `ELEVENLABS_API_KEY`
- `ELEVENLABS_VOICE_ID`
- `ELEVENLABS_MODEL_ID`
- `RVC_MODEL_REPO`
- `RVC_MODEL_FILENAME`
- `RVC_INDEX_FILENAME`
- `RVC_INFER_SCRIPT`

## Frontend Setup
1. Install dependencies:
   - `npm install` (inside `frontend`)
2. Copy `frontend/.env.example` to `frontend/.env`.
3. Start:
   - `npm run dev`

## API Endpoints
- POST /upload-pdf
- GET /summary
- GET /concepts
- GET /flashcards
- GET /quiz
- POST /transcribe
- POST /chat
- POST /voice-chat (multipart upload: audio file)
- POST /braille
- GET/POST /accessibility

## Pipelines

### Document Pipeline
Upload PDF → pdfplumber extraction → OCR fallback (pytesseract) → chunking (~500 tokens) → Gemini embeddings in FAISS → summary/concepts/flashcards/quiz + RAG tutor chat.

### Voice Pipeline
User Speech → wav2vec2 STT → Gemini Tutor → ElevenLabs TTS → RVC conversion → audio response.

## Notes
- For braille hardware output, POST `/braille` with `text` and optional `port` (for example `COM3`).
- If `port` is omitted, backend returns converted braille text only.
- Frontend voice controls support microphone recording and audio file upload to `/voice-chat`.
