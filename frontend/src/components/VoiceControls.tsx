import React, { useRef, useState } from 'react';

import api from '../api/client';

type Props = {
  defaultText: string;
  speed: number;
};

export default function VoiceControls({ defaultText, speed }: Readonly<Props>) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<Blob[]>([]);

  const [text, setText] = useState(defaultText);
  const [braillePort, setBraillePort] = useState('');
  const [brailleStatus, setBrailleStatus] = useState('');
  const [recording, setRecording] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState('');
  const [selectedAudio, setSelectedAudio] = useState<File | null>(null);

  const handleTextChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setText(e.target.value);
  };

  const handleBraillePortChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setBraillePort(e.target.value);
  };

  const handleAudioSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedAudio(e.target.files?.[0] ?? null);
  };

  const playAudioBlob = async (blob: Blob) => {
    const url = URL.createObjectURL(blob);
    if (audioRef.current) {
      audioRef.current.src = url;
      await audioRef.current.play();
    }
  };

  const sendVoiceFile = async (audioBlob: Blob, filename = 'speech.webm') => {
    const form = new FormData();
    form.append('file', new File([audioBlob], filename, { type: audioBlob.type || 'audio/webm' }));

    const response = await api.post('/voice-chat', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      responseType: 'blob',
    });

    await playAudioBlob(response.data);
    const transcript = decodeURIComponent(response.headers['x-transcript'] || '');
    setVoiceStatus(transcript ? `You said: ${transcript}` : 'Voice response generated.');
  };

  const askWithSelectedAudio = async () => {
    if (!selectedAudio) {
      setVoiceStatus('Please choose an audio file first.');
      return;
    }

    try {
      setVoiceStatus('Processing audio...');
      await sendVoiceFile(selectedAudio, selectedAudio.name);
    } catch (error: unknown) {
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setVoiceStatus(`Error: ${message || 'Voice request failed'}`);
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      chunksRef.current = [];
      mediaRecorderRef.current = mediaRecorder;

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' });
        setRecording(false);
        setVoiceStatus('Processing recording...');
        try {
          await sendVoiceFile(blob);
        } catch (error: unknown) {
          const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
          setVoiceStatus(`Error: ${message || 'Voice request failed'}`);
        }
      };

      mediaRecorder.start();
      setRecording(true);
      setVoiceStatus('Recording...');
    } catch {
      setVoiceStatus('Microphone permission denied or unavailable.');
    }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    mediaRecorderRef.current?.stream.getTracks().forEach((track) => track.stop());
  };

  const sendBraille = async () => {
    const payload: { text: string; port?: string } = { text };
    if (braillePort.trim()) {
      payload.port = braillePort.trim();
    }

    const res = await api.post('/braille', payload);
    setBrailleStatus(res.data.status === 'sent' ? `Sent to ${braillePort || 'default port'}` : 'Braille converted');
  };

  return (
    <div className="rounded-xl bg-white p-4 shadow-md dark:bg-slate-800">
      <h2 className="mb-3 text-lg font-semibold">Voice Tutor</h2>

      <div className="mb-3 flex flex-wrap gap-2">
        {recording ? (
          <button onClick={stopRecording} className="rounded bg-rose-600 px-4 py-2 text-white hover:bg-rose-700">
            Stop mic
          </button>
        ) : (
          <button onClick={startRecording} className="rounded bg-indigo-600 px-4 py-2 text-white hover:bg-indigo-700">
            Start mic
          </button>
        )}

        <input type="file" accept="audio/*" onChange={handleAudioSelect} className="rounded border px-3 py-2 text-sm" />
        <button onClick={askWithSelectedAudio} className="rounded bg-violet-600 px-4 py-2 text-white hover:bg-violet-700">
          Send audio file
        </button>
      </div>

      <p className="mb-3 text-xs text-slate-600 dark:text-slate-300">{voiceStatus}</p>

      <textarea
        className="mb-2 w-full rounded border p-2"
        rows={3}
        value={text}
        onChange={handleTextChange}
        placeholder="Text for braille output"
      />
      <div className="flex flex-wrap gap-2">
        <input
          className="rounded border px-3 py-2 text-sm"
          placeholder="Braille COM port (optional)"
          value={braillePort}
          onChange={handleBraillePortChange}
        />
        <button onClick={sendBraille} className="rounded bg-amber-600 px-4 py-2 text-white hover:bg-amber-700">
          Send braille
        </button>
      </div>

      <p className="mt-2 text-xs text-slate-600 dark:text-slate-300">{brailleStatus} | speed: {speed.toFixed(2)}</p>
      <audio ref={audioRef} className="mt-3 w-full" controls>
        <track kind="captions" />
      </audio>
    </div>
  );
}
