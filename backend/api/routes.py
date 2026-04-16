from __future__ import annotations

import asyncio
import base64
import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from typing import Annotated
from urllib.parse import quote
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse

from models.document_model import (
    AccessibilitySettings,
    BrailleRequest,
    ChatRequest,
    StoredDocument,
)
from services.adaptive_quiz import AdaptiveQuiz, AdaptiveQuizError
from services.ai_agent import NeuroLearnAgent
from services.braille_service import BrailleService, BrailleServiceError
from services.cache_manager import CacheManager
from services.command_agent import CommandAgent
from services.emotion_detector import EmotionDetector
from services.evaluation_agent import EvaluationAgent
from services.flashcard_generator import FlashcardGenerator
from services.gemini_service import GeminiService, GeminiServiceError
from services.knowledge_agent import KnowledgeAgent
from services.multi_agent_tutor import (
    MultiAgentSession,
    MultiAgentTutor,
    MultiAgentTutorError,
)
from services.pdf_processor import (
    PDFProcessingError,
    chunk_document,
    extract_text_from_pdf,
)
from services.quiz_generator import QuizGenerator
from services.rag_service import RAGService
from services.rvc_service import RVCService
from services.stt_service import STTService, STTServiceError
from services.tts_service import TTSService
from services.tutor_agent import TutorAgent, TutorAgentError, TutorState
from services.command_parser import parse_voice_command
from services.vector_store import VectorStore, VectorStoreError
from services.voice_agent import VoiceAgent
from services.voice_pipeline import VoicePipeline, VoicePipelineError
from services.voice_streamer import VoiceStreamer, VoiceStreamerError
from services.video_service import VideoService, VideoServiceError

logger = logging.getLogger(__name__)

router = APIRouter()


@dataclass
class ServiceContainer:
    vector_store: VectorStore
    gemini: GeminiService
    flashcards: FlashcardGenerator
    quiz: QuizGenerator
    rag: RAGService
    stt: STTService
    tts: TTSService
    rvc: RVCService
    voice_pipeline: VoicePipeline
    voice_streamer: VoiceStreamer
    ai_agent: NeuroLearnAgent
    command_agent: CommandAgent
    knowledge_agent: KnowledgeAgent
    evaluation_agent: EvaluationAgent
    voice_agent: VoiceAgent
    multi_agent_tutor: MultiAgentTutor
    cache: CacheManager
    adaptive_quiz: AdaptiveQuiz
    emotion_detector: EmotionDetector
    tutor_agent: TutorAgent
    braille: BrailleService
    video: VideoService
    tutor_state: TutorState = field(default_factory=TutorState)
    current_document: StoredDocument | None = None
    current_summary: str = ""
    current_concepts: list[dict[str, str]] = field(default_factory=list)
    current_flashcards: list[dict[str, str]] = field(default_factory=list)
    current_quiz: list[dict[str, Any]] = field(default_factory=list)
    current_explanation: str = ""
    current_explanation_audio: str = ""
    current_file_hash: str = ""
    processing_status: dict[str, str | int] = field(
        default_factory=lambda: {"step": "idle", "progress": 0}
    )
    multi_agent_session: MultiAgentSession = field(default_factory=MultiAgentSession)
    accessibility: AccessibilitySettings = field(default_factory=AccessibilitySettings)


_vector_store = VectorStore(storage_dir="data")
_gemini = GeminiService()
_rag = RAGService(_vector_store, _gemini)
_stt = STTService()
_tts = TTSService()
_rvc = RVCService()
_adaptive_quiz = AdaptiveQuiz(_gemini)
_emotion_detector = EmotionDetector()
_voice_pipeline = VoicePipeline(_stt, _gemini, _tts, _rvc)
_voice_streamer = VoiceStreamer(_gemini, _tts, _rvc)
_video = VideoService()
_cache = CacheManager(cache_dir="data/cache")
_ai_agent = NeuroLearnAgent()
_command_agent = CommandAgent()
_knowledge_agent = KnowledgeAgent(_gemini, _vector_store)
_evaluation_agent = EvaluationAgent(_gemini)
_voice_agent = VoiceAgent(_voice_pipeline)
_multi_agent_tutor = MultiAgentTutor(
    _command_agent, _knowledge_agent, None, _evaluation_agent, _voice_agent
)

services = ServiceContainer(
    vector_store=_vector_store,
    gemini=_gemini,
    flashcards=FlashcardGenerator(_gemini),
    quiz=QuizGenerator(_gemini),
    rag=_rag,
    stt=_stt,
    tts=_tts,
    rvc=_rvc,
    voice_pipeline=_voice_pipeline,
    voice_streamer=_voice_streamer,
    ai_agent=_ai_agent,
    command_agent=_command_agent,
    knowledge_agent=_knowledge_agent,
    evaluation_agent=_evaluation_agent,
    voice_agent=_voice_agent,
    multi_agent_tutor=_multi_agent_tutor,
    cache=_cache,
    adaptive_quiz=_adaptive_quiz,
    emotion_detector=_emotion_detector,
    tutor_agent=None,
    braille=BrailleService(),
    video=_video,
)


def _get_tutor_agent():
    if services.tutor_agent is None:
        logger.info("Initializing TutorAgent lazily...")
        services.tutor_agent = TutorAgent(
            services.gemini,
            services.voice_pipeline,
            services.adaptive_quiz,
            services.emotion_detector,
            services.voice_streamer,
        )
        services.tutor_agent.voice_pipeline = services.voice_pipeline
        services.multi_agent_tutor.tutor_agent = services.tutor_agent
    return services.tutor_agent


def _get_multi_agent_tutor():
    _get_tutor_agent()
    return services.multi_agent_tutor


voice_output_dir = Path("data") / "voice_outputs"
voice_output_dir.mkdir(parents=True, exist_ok=True)


@router.post(
    "/upload-pdf",
    responses={
        400: {"description": "Invalid file"},
        422: {"description": "Unprocessable PDF"},
        500: {"description": "Server error"},
        502: {"description": "AI voice generation failure"},
    },
)
async def upload_pdf(
    background_tasks: BackgroundTasks, file: Annotated[UploadFile, File(...)]
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400, detail="Invalid file type. Please upload a PDF."
        )

    try:
        services.processing_status = {"step": "extracting_text", "progress": 10}
        file_bytes = await file.read()
        file_hash = services.cache.hash_bytes(file_bytes)
        cached = services.cache.get(file_hash)

        if cached is not None:
            _hydrate_services_from_cache(cached)
            services.current_file_hash = file_hash
            services.processing_status = {"step": "done", "progress": 100}
            return {
                "status": "ok",
                "cached": True,
                "filename": file.filename,
                "text_length": len(
                    services.current_document.text if services.current_document else ""
                ),
                "chunks": len(
                    services.current_document.chunks
                    if services.current_document
                    else []
                ),
                "chunk_count": len(
                    services.current_document.chunks
                    if services.current_document
                    else []
                ),
                "summary": services.current_summary,
                "concepts": services.current_concepts,
                "flashcards": services.current_flashcards,
                "quiz": services.current_quiz,
                "explanation": services.current_explanation,
                "voice_explanation": services.current_explanation_audio,
                "tutor_greeting": "Hello! I will explain this document and help you learn it.",
            }

        text = extract_text_from_pdf(file_bytes)
        chunks = chunk_document(text, chunk_size_tokens=500, overlap_tokens=50)
        background_tasks.add_task(
            services.vector_store.store_embeddings_background,
            [c.model_dump() for c in chunks],
        )

        services.current_document = StoredDocument(
            filename=file.filename,
            text=text,
            chunks=chunks,
        )

        services.processing_status = {"step": "understanding_document", "progress": 45}
        summary_error = ""
        try:
            summary = await asyncio.to_thread(services.gemini.generate_summary, text)
        except GeminiServiceError as ex:
            summary_error = str(ex)
            summary = _fallback_summary(text)

        services.processing_status = {
            "step": "generating_learning_materials",
            "progress": 70,
        }
        concepts_task = asyncio.to_thread(services.gemini.generate_concepts, summary)
        flashcards_task = asyncio.to_thread(services.flashcards.generate, summary)
        quiz_task = asyncio.to_thread(services.quiz.generate, summary)
        explanation_task = asyncio.to_thread(
            services.gemini.tutor_chat,
            f"Explain this summary clearly for a student:\n\n{summary}",
        )

        concepts, flashcards, quiz, explanation = await asyncio.gather(
            concepts_task,
            flashcards_task,
            quiz_task,
            explanation_task,
            return_exceptions=True,
        )

        concepts = concepts if isinstance(concepts, list) else []
        flashcards = flashcards if isinstance(flashcards, list) else []
        quiz = quiz if isinstance(quiz, list) else []
        explanation = (
            explanation
            if isinstance(explanation, str) and explanation.strip()
            else summary
        )

        if not concepts:
            concepts = _fallback_concepts(summary)
        if not flashcards:
            flashcards = _fallback_flashcards(summary)
        if not quiz:
            quiz = _fallback_quiz(summary)

        audio_path = ""
        voice_error = ""

        try:
            voice_result = await services.voice_pipeline.explain_document(explanation)
            explanation = str(voice_result["explanation"] or explanation)
            audio_path = _persist_audio_bytes(
                voice_result["audio"], prefix="explanation"
            )
        except VoicePipelineError as ex:
            voice_error = str(ex)

        services.current_summary = summary
        services.current_concepts = concepts
        services.current_flashcards = flashcards
        services.current_quiz = quiz
        services.current_explanation = explanation
        services.current_explanation_audio = audio_path
        services.current_file_hash = file_hash
        services.processing_status = {"step": "done", "progress": 100}

        services.cache.set(
            file_hash,
            {
                "filename": file.filename,
                "text": text,
                "chunks": [c.model_dump() for c in chunks],
                "summary": summary,
                "concepts": concepts,
                "flashcards": flashcards,
                "quiz": quiz,
                "explanation": explanation,
                "voice_explanation": audio_path,
            },
        )

        return {
            "status": "ok",
            "cached": False,
            "filename": file.filename,
            "text_length": len(text),
            "chunks": len(chunks),
            "chunk_count": len(chunks),
            "summary": summary,
            "concepts": concepts,
            "flashcards": flashcards,
            "quiz": quiz,
            "explanation": explanation,
            "voice_explanation": audio_path,
            "tutor_greeting": "Hello! I will explain this document and help you learn it.",
            "voice_warning": voice_error,
            "summary_warning": summary_error,
            "processing": services.processing_status,
        }
    except PDFProcessingError as ex:
        raise HTTPException(status_code=422, detail=str(ex)) from ex
    except VectorStoreError as ex:
        raise HTTPException(status_code=500, detail=str(ex)) from ex
    except Exception as ex:
        raise HTTPException(
            status_code=500, detail=f"Unexpected upload error: {ex}"
        ) from ex


@router.post(
    "/upload",
    include_in_schema=False,
    responses={
        400: {"description": "Invalid file"},
        422: {"description": "Unprocessable PDF"},
        500: {"description": "Server error"},
        502: {"description": "AI voice generation failure"},
    },
)
async def upload_pdf_legacy(file: Annotated[UploadFile, File(...)]):
    bg = BackgroundTasks()
    return await upload_pdf(bg, file)


@router.get(
    "/summary",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "AI service failure"},
    },
)
def get_summary():
    _require_document()
    return {"summary": services.current_summary}


@router.get(
    "/concepts",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "AI service failure"},
    },
)
def get_concepts():
    _require_document()
    return {"concepts": services.current_concepts}


@router.get(
    "/flashcards",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "AI service failure"},
    },
)
def get_flashcards():
    _require_document()
    return {"flashcards": services.current_flashcards}


@router.get(
    "/quiz",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "AI service failure"},
    },
)
def get_quiz():
    _require_document()
    return {"quiz": services.current_quiz}


@router.post(
    "/chat",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "AI/RAG failure"},
    },
)
def post_chat(payload: ChatRequest):
    try:
        if services.current_document is not None:
            response = services.rag.answer_question(payload.question)
        else:
            response = {
                "answer": services.gemini.tutor_chat(payload.question),
                "sources": [],
            }
        return response
    except (VectorStoreError, GeminiServiceError) as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/voice-chat",
    responses={
        400: {"description": "Invalid audio file"},
        502: {"description": "Voice pipeline failure"},
    },
)
async def post_voice_chat(file: Annotated[UploadFile, File(...)]):
    try:
        audio_bytes = await file.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Uploaded audio is empty.")

        result = services.voice_pipeline.run(audio_bytes)
        headers = {
            "X-Transcript": quote(str(result["transcript"]))[:500],
            "X-Answer-Preview": quote(str(result["answer"])[:220]),
        }
        return StreamingResponse(
            iter([result["audio"]]), media_type="audio/wav", headers=headers
        )
    except VoicePipelineError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/tutor-conversation",
    responses={
        400: {"description": "Invalid question"},
        502: {"description": "Tutor generation failure"},
    },
)
async def post_tutor_conversation(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    context = (
        services.current_document.text if services.current_document is not None else ""
    )
    try:
        result = await _get_tutor_agent().tutor_conversation(payload.question, context)
        audio_path = _persist_audio_bytes(result["audio"], prefix="conversation")
        return {
            "response": result["response"],
            "voice": audio_path,
        }
    except TutorAgentError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/tutor-turn",
    responses={
        400: {"description": "Invalid tutor input"},
        502: {"description": "Tutor loop failure"},
    },
)
async def post_tutor_turn(payload: dict):
    question = str(payload.get("question", ""))
    student_answer = str(payload.get("student_answer", ""))
    context = (
        services.current_document.text
        if services.current_document is not None
        else str(payload.get("context", ""))
    )
    if not question.strip() and not student_answer.strip():
        raise HTTPException(
            status_code=400, detail="Provide question or student_answer."
        )

    try:
        result = await _get_tutor_agent().tutor_turn(
            question=question,
            context=context,
            state=services.tutor_state,
            student_answer=student_answer,
        )
        audio_path = _persist_audio_bytes(
            services.voice_pipeline.synthesize_tutor_audio(str(result["response"])),
            prefix="tutor_turn",
        )
        return {
            **result,
            "voice": audio_path,
        }
    except TutorAgentError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/adaptive-quiz",
    responses={
        400: {"description": "No context available"},
        502: {"description": "Adaptive quiz failure"},
    },
)
def post_adaptive_quiz(payload: dict):
    difficulty = str(payload.get("difficulty", services.tutor_state.difficulty))
    context = (
        services.current_document.text
        if services.current_document is not None
        else str(payload.get("context", ""))
    )
    if not context.strip():
        raise HTTPException(
            status_code=400, detail="No context available for adaptive quiz."
        )

    try:
        q = services.adaptive_quiz.generate_question(
            context=context, difficulty=difficulty
        )
        services.tutor_state.difficulty = q.difficulty
        services.tutor_state.last_question = q.question
        services.tutor_state.expected_answer = q.expected_answer
        return {
            "difficulty": q.difficulty,
            "question": q.question,
            "expected_answer": q.expected_answer,
        }
    except AdaptiveQuizError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.get(
    "/voice-stream-explanation",
    responses={
        400: {"description": "No document uploaded"},
        502: {"description": "Streaming voice failure"},
    },
)
async def get_voice_stream_explanation():
    _require_document()
    context = services.current_summary or (
        services.current_document.text if services.current_document else ""
    )

    async def ndjson_stream():
        yield (
            json.dumps({"type": "start", "message": "Streaming explanation started."})
            + "\n"
        )
        async for stream_chunk in services.voice_streamer.stream_explanation(context):
            audio_path = _persist_audio_bytes(
                stream_chunk.audio, prefix=f"stream_{stream_chunk.index}"
            )
            payload = {
                "type": "chunk",
                "index": stream_chunk.index,
                "text": stream_chunk.text,
                "audio": audio_path,
                "audio_b64": base64.b64encode(stream_chunk.audio).decode("utf-8"),
            }
            yield json.dumps(payload) + "\n"
        yield json.dumps({"type": "done"}) + "\n"

    try:
        return StreamingResponse(ndjson_stream(), media_type="application/x-ndjson")
    except VoiceStreamerError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/tutor-conversation-stream",
    responses={
        400: {"description": "Invalid question"},
        502: {"description": "Tutor stream failure"},
    },
)
async def post_tutor_conversation_stream(payload: ChatRequest):
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")
    context = services.current_summary or (
        services.current_document.text if services.current_document else ""
    )

    async def ndjson_stream():
        async for chunk in _get_tutor_agent().tutor_conversation_stream(
            payload.question, context
        ):
            yield json.dumps({"type": "text", **chunk}) + "\n"

    try:
        return StreamingResponse(ndjson_stream(), media_type="application/x-ndjson")
    except TutorAgentError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.get(
    "/demo-mode/start", responses={502: {"description": "Demo greeting failure"}}
)
async def start_demo_mode():
    greeting = "Welcome to NeuroLearn Assist. Your AI tutor is ready to help you learn."
    hello = "Hello, I am your NeuroLearn AI Tutor. Please upload your document."
    try:
        audio_bytes = await services.voice_streamer.greeting_audio(
            f"{greeting} {hello}"
        )
        audio_path = _persist_audio_bytes(audio_bytes, prefix="demo_greeting")
        return {
            "message": greeting,
            "hello": hello,
            "voice": audio_path,
        }
    except VoiceStreamerError as ex:
        return {
            "message": greeting,
            "hello": hello,
            "voice": "",
            "warning": str(ex),
        }


@router.post("/voice-command")
def post_voice_command(payload: dict):
    command_text = str(payload.get("command", ""))
    parsed = parse_voice_command(command_text)
    return {
        "action": parsed.action,
        "command": parsed.normalized_text,
        "requires_wake_word": parsed.requires_wake_word,
    }


@router.post("/agent-command")
def post_agent_command(payload: dict):
    text = str(payload.get("command", ""))
    result = services.ai_agent.handle_command(text)
    return {
        "intent": result.intent,
        "action": result.action,
        "response": result.response,
        "requires_wake_word": result.requires_wake_word,
    }


@router.post(
    "/multi-agent/handle",
    responses={502: {"description": "Multi-agent processing failure"}},
)
async def post_multi_agent_handle(payload: dict):
    user_text = str(payload.get("command", ""))
    student_answer = str(payload.get("answer", ""))
    context = (
        services.current_document.text if services.current_document is not None else ""
    )

    try:
        result = await services.multi_agent_tutor.handle(
            session=services.multi_agent_session,
            user_text=user_text,
            document_text=context,
            student_answer=student_answer,
        )
        audio = result.get("audio", b"")
        audio_path = (
            _persist_audio_bytes(audio, prefix="multi_agent")
            if isinstance(audio, (bytes, bytearray)) and len(audio) > 0
            else ""
        )
        return {
            **{k: v for k, v in result.items() if k != "audio"},
            "voice": audio_path,
        }
    except MultiAgentTutorError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.get(
    "/voice-file/{file_name}", responses={404: {"description": "Voice file not found"}}
)
def get_voice_file(file_name: str):
    file_path = voice_output_dir / file_name
    return FileResponse(path=str(file_path), media_type="audio/wav", filename=file_name)


@router.get("/download-mp4")
async def download_mp4():
    _require_document()
    if not services.current_explanation:
        raise HTTPException(status_code=400, detail="No explanation generated yet.")
    
    # Resolve the audio file
    audio_file_name = services.current_explanation_audio.split('/')[-1]
    audio_path = voice_output_dir / audio_file_name
    
    if not audio_path.exists():
        # Regeneration fallback if file is missing
        try:
            voice_result = await services.voice_pipeline.explain_document(services.current_explanation)
            audio_bytes = voice_result["audio"]
        except Exception as e:
            raise HTTPException(status_code=502, detail=f"Audio retrieval failed: {e}")
    else:
        audio_bytes = audio_path.read_bytes()

    try:
        # Generate the video
        video_path = services.video.generate_explanation_mp4(
            services.current_explanation, 
            audio_bytes
        )
        return FileResponse(
            path=video_path, 
            media_type="video/mp4", 
            filename="explanation.mp4"
        )
    except VideoServiceError as ex:
        raise HTTPException(status_code=500, detail=str(ex))


@router.post(
    "/voice",
    include_in_schema=False,
    responses={
        400: {"description": "Invalid audio file"},
        502: {"description": "Voice pipeline failure"},
    },
)
async def post_voice_legacy(file: Annotated[UploadFile, File(...)]):
    return await post_voice_chat(file)


@router.post(
    "/transcribe",
    responses={
        400: {"description": "Invalid audio file"},
        502: {"description": "Transcription failure"},
    },
)
async def transcribe_audio(file: Annotated[UploadFile, File(...)]):
    try:
        audio_bytes = await file.read()
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Uploaded audio is empty.")
        transcript = services.stt.transcribe_audio(audio_bytes)
        return {"transcript": transcript}
    except STTServiceError as ex:
        raise HTTPException(status_code=502, detail=str(ex)) from ex


@router.post(
    "/braille", responses={503: {"description": "Braille hardware unavailable"}}
)
def post_braille(payload: BrailleRequest):
    try:
        if payload.port:
            result = services.braille.send_to_arduino(
                payload.text, port=payload.port, baud_rate=payload.baud_rate
            )
            return {
                "status": "sent",
                "braille_text": result.braille_text,
                "bytes_sent": result.bytes_sent,
            }

        braille_text = services.braille.text_to_braille(payload.text)
        return {"status": "converted", "braille_text": braille_text}
    except BrailleServiceError as ex:
        raise HTTPException(status_code=503, detail=str(ex)) from ex


@router.post(
    "/braille-output", responses={503: {"description": "Braille hardware unavailable"}}
)
def post_braille_output(payload: BrailleRequest):
    return post_braille(payload)


@router.get("/processing-status")
def get_processing_status():
    return services.processing_status


@router.get("/accessibility")
def get_accessibility_settings():
    return services.accessibility.model_dump()


@router.post("/accessibility")
def update_accessibility_settings(settings: AccessibilitySettings):
    services.accessibility = settings
    return {"status": "ok", "settings": services.accessibility.model_dump()}


def _require_document() -> StoredDocument:
    if services.current_document is None:
        raise HTTPException(status_code=400, detail="No document uploaded yet.")
    return services.current_document


def _persist_audio_bytes(audio_bytes: bytes | str, prefix: str) -> str:
    if isinstance(audio_bytes, str):
        data = audio_bytes.encode("utf-8")
    else:
        data = audio_bytes
    file_name = f"{prefix}_{uuid4().hex}.wav"
    path = voice_output_dir / file_name
    path.write_bytes(data)
    return f"/voice-file/{file_name}"


def _fallback_summary(text: str) -> str:
    clean = " ".join(text.split())
    short = clean[:900]
    return (
        "Quick document overview (fallback):\n"
        f"{short}\n\n"
        "I can still help you study this content even when the AI summary service is temporarily unavailable."
    )


def _fallback_concepts(summary: str) -> list[dict[str, str]]:
    sentences = [s.strip() for s in summary.replace("\n", " ").split(".") if s.strip()]
    selected = sentences[:4] or [summary[:180]]
    concepts: list[dict[str, str]] = []
    for i, sentence in enumerate(selected, start=1):
        concepts.append({"concept": f"Core Idea {i}", "explanation": sentence[:220]})
    return concepts


def _fallback_flashcards(summary: str) -> list[dict[str, str]]:
    concepts = _fallback_concepts(summary)
    return [
        {
            "question": f"What is the key point of {item['concept']}?",
            "answer": item["explanation"],
        }
        for item in concepts
    ]


def _fallback_quiz(summary: str) -> list[dict[str, Any]]:
    concept = _fallback_concepts(summary)[0]
    return [
        {
            "question": f"Which option best matches {concept['concept']}?",
            "options": [
                concept["explanation"],
                "It is unrelated to the topic.",
                "It only describes file metadata.",
                "It is a random placeholder.",
            ],
            "correct_answer": concept["explanation"],
            "explanation": "Generated from fallback mode to keep learning flow fast.",
        }
    ]


def _hydrate_services_from_cache(cached: dict[str, Any]) -> None:
    text = str(cached.get("text", ""))
    chunks_data = cached.get("chunks", []) or []
    # Build chunk models without importing extra symbols repeatedly.
    from models.document_model import DocumentChunk

    hydrated_chunks = [DocumentChunk(**c) for c in chunks_data]
    services.current_document = StoredDocument(
        filename=str(cached.get("filename", "cached.pdf")),
        text=text,
        chunks=hydrated_chunks,
    )
    services.current_summary = str(cached.get("summary", ""))
    services.current_concepts = list(cached.get("concepts", []))
    services.current_flashcards = list(cached.get("flashcards", []))
    services.current_quiz = list(cached.get("quiz", []))
    services.current_explanation = str(
        cached.get("explanation", services.current_summary)
    )
    services.current_explanation_audio = str(cached.get("voice_explanation", ""))
