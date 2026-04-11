import React, { useEffect, useRef, useState } from 'react';

import api from '../api/client';

type LocalSpeechRecognitionAlternative = {
  transcript: string;
};

type LocalSpeechRecognitionResult = {
  0: LocalSpeechRecognitionAlternative;
};

type LocalSpeechRecognitionEvent = {
  results: LocalSpeechRecognitionResult[];
};

type LocalSpeechRecognition = {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: LocalSpeechRecognitionEvent) => void) | null;
  onerror: (() => void) | null;
  start: () => void;
  stop: () => void;
};

declare global {
  interface Window {
    webkitSpeechRecognition?: new () => LocalSpeechRecognition;
  }
}

export default function VoiceTutor() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const recognitionRef = useRef<LocalSpeechRecognition | null>(null);
  const audioQueueRef = useRef<string[]>([]);
  const audioPlayingRef = useRef(false);

  const [recording, setRecording] = useState(false);
  const [listeningCommand, setListeningCommand] = useState(false);
  const [status, setStatus] = useState('');
  const [transcript, setTranscript] = useState('');
  const [streamingExplain, setStreamingExplain] = useState(false);
  const [messages, setMessages] = useState<Array<{ role: 'ai' | 'user'; text: string }>>([]);
  const [assistantArmed, setAssistantArmed] = useState(false);

  const welcomeSpokenRef = useRef(false);

  const speakLocal = (message: string) => {
    if (!('speechSynthesis' in globalThis)) return;
    const utterance = new SpeechSynthesisUtterance(message);
    utterance.rate = 1;
    globalThis.speechSynthesis.speak(utterance);
  };

  useEffect(() => {
    if (welcomeSpokenRef.current) return;
    welcomeSpokenRef.current = true;
    void runDemoGreeting();
  }, []);

  const runDemoGreeting = async () => {
    try {
      const res = await api.get('/demo-mode/start');
      const voice = res.data?.voice as string | undefined;
      if (voice && audioRef.current) {
        audioRef.current.src = `${api.defaults.baseURL}${voice}`;
        await audioRef.current.play();
      } else {
        speakLocal('Hello. I am NeuroLearn AI. Your intelligent tutor assistant. How can I help you today?');
      }
    } catch {
      speakLocal('Hello. I am NeuroLearn AI. Your intelligent tutor assistant. How can I help you today?');
    }
  };

  const enqueueAudio = (audioPath: string) => {
    audioQueueRef.current.push(audioPath);
    void playAudioQueue();
  };

  const playAudioQueue = async () => {
    if (audioPlayingRef.current || !audioRef.current) return;
    audioPlayingRef.current = true;
    try {
      while (audioQueueRef.current.length > 0 && audioRef.current) {
        const next = audioQueueRef.current.shift();
        if (!next) continue;
        audioRef.current.src = next.startsWith('http') ? next : `${api.defaults.baseURL}${next}`;
        await audioRef.current.play();
        await new Promise<void>((resolve) => {
          if (!audioRef.current) {
            resolve();
            return;
          }
          const onEnded = () => {
            audioRef.current?.removeEventListener('ended', onEnded);
            resolve();
          };
          audioRef.current.addEventListener('ended', onEnded);
        });
      }
    } finally {
      audioPlayingRef.current = false;
    }
  };

  const streamExplanation = async () => {
    setStreamingExplain(true);
    setStatus('Starting streaming explanation...');

    try {
      const response = await fetch(`${api.defaults.baseURL}/voice-stream-explanation`);
      if (!response.ok || !response.body) {
        throw new Error('Streaming endpoint unavailable.');
      }
      await consumeExplanationStream(response.body);
    } catch {
      setStatus('Streaming explanation failed.');
    } finally {
      setStreamingExplain(false);
    }
  };

  const consumeExplanationStream = async (body: ReadableStream<Uint8Array>) => {
    const reader = body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) return;
      buffer += decoder.decode(value, { stream: true });
      buffer = await processBufferedLines(buffer);
    }
  };

  const processBufferedLines = async (buffer: string) => {
    let nextBuffer = buffer;
    let newlineIndex = nextBuffer.indexOf('\n');

    while (newlineIndex >= 0) {
      const line = nextBuffer.slice(0, newlineIndex).trim();
      nextBuffer = nextBuffer.slice(newlineIndex + 1);
      if (line) {
        const evt = JSON.parse(line) as { type?: string; audio?: string; text?: string };
        await handleStreamEvent(evt);
      }
      newlineIndex = nextBuffer.indexOf('\n');
    }

    return nextBuffer;
  };

  const handleStreamEvent = async (evt: { type?: string; audio?: string; text?: string }) => {
    if (evt.type === 'chunk') {
      const streamText = evt.text ?? '';
      if (streamText) {
        setMessages((prev) => [...prev, { role: 'ai', text: streamText }]);
      }
      if (evt.audio) {
        enqueueAudio(evt.audio);
      }
      setStatus(evt.text ? `Tutor: ${evt.text}` : 'Streaming tutor explanation...');
      return;
    }

    if (evt.type === 'done') {
      setStatus('Streaming explanation completed.');
    }
  };

  const playResponse = async (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    if (audioRef.current) {
      audioRef.current.src = url;
      await audioRef.current.play();
    }
  };

  const sendAudio = async (blob: Blob) => {
    const form = new FormData();
    form.append('file', new File([blob], 'voice.webm', { type: blob.type || 'audio/webm' }));

    const response = await api.post('/voice-chat', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      responseType: 'blob',
    });

    const heard = decodeURIComponent(response.headers['x-transcript'] || '');
    if (heard) {
      setTranscript(heard);
      setMessages((prev) => [...prev, { role: 'user', text: heard }]);
    }
    await playResponse(response.data);
    const aiPreview = decodeURIComponent(response.headers['x-answer-preview'] || 'Tutor response ready.');
    setMessages((prev) => [...prev, { role: 'ai', text: aiPreview }]);
    setStatus('Tutor response ready.');
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      recorderRef.current = recorder;
      chunksRef.current = [];

      recorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      recorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setRecording(false);
        setStatus('Processing...');
        try {
          await sendAudio(blob);
        } catch (error: unknown) {
          const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
          setStatus(`Error: ${message || 'Voice chat failed'}`);
        }
      };

      recorder.start();
      setRecording(true);
      setStatus('Recording...');
    } catch {
      setStatus('Microphone unavailable or permission denied.');
    }
  };

  const stopRecording = () => {
    recorderRef.current?.stop();
    recorderRef.current?.stream.getTracks().forEach((track) => track.stop());
  };

  const handleVoiceAction = (action: string) => {
    if (action === 'UPLOAD') {
      document.getElementById('pdf-upload-input')?.click();
      setStatus('Opening file picker...');
      return;
    }

    if (action === 'QUIZ') {
      document.getElementById('quiz-section')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setStatus('Opening quiz section...');
      return;
    }

    if (action === 'FLASHCARDS') {
      document.getElementById('flashcards')?.scrollIntoView({ behavior: 'smooth', block: 'start' });
      setStatus('Opening flashcards...');
      return;
    }

    if (action === 'EXPLAIN' || action === 'REPEAT') {
      const voiceUrl = localStorage.getItem('neurolearn_voice_explanation');
      if (voiceUrl && audioRef.current) {
        audioRef.current.src = voiceUrl;
        void audioRef.current.play();
        setStatus('Replaying explanation...');
      } else {
        void streamExplanation();
      }
      return;
    }

    if (action === 'NEXT') {
      setStatus('Ask your next question using voice chat.');
      return;
    }

    if (action === 'PAUSE') {
      audioRef.current?.pause();
      setStatus('Tutor paused.');
      return;
    }

    setStatus('Command not recognized.');
  };

  const startCommandListening = () => {
    const SpeechRecognitionCtor = globalThis.window.webkitSpeechRecognition;
    if (!SpeechRecognitionCtor) {
      setStatus('Browser speech recognition is not supported here.');
      return;
    }

    const recognition = new SpeechRecognitionCtor();
    recognitionRef.current = recognition;
    recognition.lang = 'en-US';
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onresult = (event: LocalSpeechRecognitionEvent) => {
      const command = event.results[0]?.[0]?.transcript?.trim() || '';
      if (!command) {
        setStatus('No command detected.');
        setListeningCommand(false);
        return;
      }

      setStatus(`Command heard: ${command}`);
      setMessages((prev) => [...prev, { role: 'user', text: command }]);
      void (async () => {
        try {
          const result = await api.post('/multi-agent/handle', { command });
          const action = result.data.action || 'CHAT';
          const responseText = result.data.response || 'Task completed. What else can I do for you?';
          const requiresWake = action === 'WAIT_WAKE';

          if (action === 'WAKE' || result.data.wake_active) {
            setAssistantArmed(true);
          }

          if (requiresWake && !assistantArmed) {
            setMessages((prev) => [...prev, { role: 'ai', text: 'Say Jarvis, NeuroLearn, or Hey Tutor to activate me.' }]);
            setStatus('Waiting for wake word...');
            return;
          }

          setMessages((prev) => [...prev, { role: 'ai', text: responseText }]);
          speakLocal(responseText);
          const voicePath = result.data.voice as string | undefined;
          if (voicePath) {
            enqueueAudio(voicePath);
          }
          handleVoiceAction(action);
        } catch {
          setStatus('Voice command request failed.');
        } finally {
          setListeningCommand(false);
        }
      })();
    };

    recognition.onerror = () => {
      setListeningCommand(false);
      setStatus('Voice command recognition error.');
    };

    setListeningCommand(true);
    recognition.start();
    setStatus('Listening for command...');
  };

  const stopCommandListening = () => {
    recognitionRef.current?.stop();
    setListeningCommand(false);
  };

  return (
    <section id="voice" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm dark:border-slate-700 dark:bg-slate-900/60">
      <div className="mb-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          <div className={`grid h-10 w-10 place-content-center rounded-full ${recording ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/30' : 'bg-slate-100 text-slate-700 dark:bg-slate-800 dark:text-slate-200'}`}>
            🤖
          </div>
          <div>
            <h2 className="text-lg font-semibold">Voice Tutor</h2>
            <p className="text-xs text-slate-500 dark:text-slate-400">AI conversation + commands + streaming explanation</p>
          </div>
        </div>

        <div className="flex items-end gap-1">
          {[1, 2, 3, 4, 5].map((b) => (
            <span key={b} className={`inline-block w-1 rounded-full bg-blue-500 ${recording || streamingExplain ? 'animate-pulse' : ''}`} style={{ height: `${8 + b * 5}px` }} />
          ))}
        </div>
      </div>

      <div className="flex flex-wrap gap-2">
        {recording ? (
          <button onClick={stopRecording} className="rounded-xl bg-rose-600 px-4 py-2 text-sm font-medium text-white hover:bg-rose-700">
            Stop chat voice
          </button>
        ) : (
          <button onClick={startRecording} className="rounded-xl bg-indigo-600 px-4 py-2 text-sm font-medium text-white hover:bg-indigo-700">
            Start chat voice
          </button>
        )}

        {listeningCommand ? (
          <button onClick={stopCommandListening} className="rounded-xl bg-orange-600 px-4 py-2 text-sm font-medium text-white hover:bg-orange-700">
            Stop command
          </button>
        ) : (
          <button onClick={startCommandListening} className="rounded-xl bg-emerald-600 px-4 py-2 text-sm font-medium text-white hover:bg-emerald-700">
            Start voice command
          </button>
        )}

        <button
          onClick={streamExplanation}
          disabled={streamingExplain}
          className="rounded-xl bg-cyan-600 px-4 py-2 text-sm font-medium text-white hover:bg-cyan-700 disabled:opacity-50"
        >
          {streamingExplain ? 'Streaming...' : 'Start explanation stream'}
        </button>
      </div>

      <div className="mt-4 max-h-56 space-y-2 overflow-y-auto rounded-xl border border-slate-200 bg-slate-50 p-3 dark:border-slate-700 dark:bg-slate-800/80">
        {messages.length === 0 && <p className="text-xs text-slate-500 dark:text-slate-400">Conversation bubbles will appear here.</p>}
        {messages.map((m, i) => (
          <div key={`${m.role}-${i}`} className={`max-w-[85%] rounded-xl px-3 py-2 text-sm ${m.role === 'ai' ? 'bg-blue-100 text-blue-900 dark:bg-blue-500/20 dark:text-blue-100' : 'ml-auto bg-slate-200 text-slate-800 dark:bg-slate-700 dark:text-slate-100'}`}>
            {m.text}
          </div>
        ))}
      </div>

      <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{status}</p>
      {transcript && <p className="mt-2 text-sm"><b>You said:</b> {transcript}</p>}
      <audio ref={audioRef} className="mt-3 w-full rounded-xl" controls>
        <track kind="captions" />
      </audio>
    </section>
  );
}
