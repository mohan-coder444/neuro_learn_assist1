import React, { useState } from 'react';
import api from '../api/client';

type UploadResponse = {
  filename: string;
  chunks: number;
  text_length?: number;
  summary?: string;
  explanation?: string;
  voice_explanation?: string;
  tutor_greeting?: string;
  summary_warning?: string;
  voice_warning?: string;
};

type Props = {
  onUploaded: (data: UploadResponse) => void;
};

export default function PDFUploader({ onUploaded }: Readonly<Props>) {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<string>('');
  const [uploadProgress, setUploadProgress] = useState(0);
  const [dragging, setDragging] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFile(e.target.files?.[0] ?? null);
  };

  const handleDrop = (e: React.DragEvent<HTMLLabelElement>) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files?.[0] ?? null;
    if (dropped?.type === 'application/pdf') {
      setFile(dropped);
      setStatus(`Selected ${dropped.name}`);
    }
  };

  const upload = async () => {
    if (!file) return;

    const data = new FormData();
    data.append('file', file);

    setStatus('Uploading...');
    setUploadProgress(8);
    const ticker = setInterval(() => {
      setUploadProgress((prev) => Math.min(prev + 8, 90));
    }, 180);

    try {
      const res = await api.post('/upload-pdf', data, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const chunkCandidate = res.data?.chunks ?? res.data?.chunk_count ?? res.data?.total_chunks ?? res.data?.num_chunks;
      const parsedChunks = Number.parseInt(String(chunkCandidate ?? ''), 10);
      const normalized: UploadResponse = {
        filename: String(res.data?.filename || file.name || 'document.pdf'),
        chunks: Number.isFinite(parsedChunks) ? parsedChunks : 0,
        text_length: Number(res.data?.text_length || 0),
        summary: res.data?.summary,
        explanation: res.data?.explanation,
        voice_explanation: res.data?.voice_explanation,
        tutor_greeting: res.data?.tutor_greeting,
        summary_warning: res.data?.summary_warning,
        voice_warning: res.data?.voice_warning,
      };

      const warnings = [normalized.summary_warning, normalized.voice_warning].filter(Boolean).length;
      const warningSuffix = warnings ? ` • ${warnings} warning(s)` : '';
      clearInterval(ticker);
      setUploadProgress(100);
      setStatus(`Uploaded ${normalized.filename} (${normalized.chunks} chunks)${warningSuffix}`);
      onUploaded(normalized);
    } catch (error: unknown) {
      clearInterval(ticker);
      setUploadProgress(0);
      const message = (error as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setStatus(`Error: ${message || 'Upload failed'}`);
      return;
    }
  };

  return (
    <section id="upload" className="rounded-2xl border border-slate-200 bg-white/90 p-5 shadow-sm transition dark:border-slate-700 dark:bg-slate-900/60">
      <h2 className="text-lg font-semibold">Upload your learning document</h2>
      <p className="mt-1 text-sm text-slate-500 dark:text-slate-400">NeuroLearn AI will extract text, summarize, and start tutor mode.</p>

      <label
        htmlFor="pdf-upload-input"
        onDrop={handleDrop}
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        className={`mt-4 rounded-2xl border-2 border-dashed p-8 text-center transition ${
          dragging
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-500/10'
            : 'border-slate-300 bg-slate-50 dark:border-slate-600 dark:bg-slate-800/60'
        }`}
      >
        <p className="text-sm font-medium">Drag file here</p>
        <p className="my-2 text-xs text-slate-500">or</p>
        <span className="inline-flex cursor-pointer rounded-xl bg-slate-900 px-4 py-2 text-sm font-medium text-white transition hover:-translate-y-0.5 dark:bg-blue-600">
          Choose file
        </span>
        <input
          id="pdf-upload-input"
          type="file"
          accept="application/pdf"
          onChange={handleFileChange}
          className="hidden"
        />
      </label>

      {file && (
        <div className="mt-4 rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm dark:border-slate-700 dark:bg-slate-800/80">
          <p className="font-medium">{file.name}</p>
          <p className="text-xs text-slate-500 dark:text-slate-400">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
        </div>
      )}

      <button
        onClick={upload}
        disabled={!file}
        className="mt-4 inline-flex rounded-xl bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-md shadow-blue-500/30 transition hover:-translate-y-0.5 hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
      >
        Upload & Analyze
      </button>

      {uploadProgress > 0 && (
        <div className="mt-3">
          <p className="mb-1 text-xs text-slate-500 dark:text-slate-400">NeuroLearn AI is analyzing your document...</p>
          <div className="h-2 w-full overflow-hidden rounded-full bg-slate-200 dark:bg-slate-700">
            <div className="h-full rounded-full bg-blue-600 transition-all duration-300" style={{ width: `${uploadProgress}%` }} />
          </div>
        </div>
      )}

      <p className="mt-3 text-sm text-slate-600 dark:text-slate-300">{status}</p>
    </section>
  );
}
