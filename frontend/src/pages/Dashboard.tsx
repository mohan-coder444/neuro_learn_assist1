import React, { useEffect, useState } from 'react';

import api from '../api/client';
import AccessibilitySettings from '../components/AccessibilitySettings';
import ConceptsViewer from '../components/ConceptsViewer';
import Flashcards from '../components/Flashcards';
import Layout from '../components/Layout';
import PDFUploader from '../components/PDFUploader';
import Quiz from '../components/Quiz';
import SummaryViewer from '../components/SummaryViewer';
import TutorChat from '../components/TutorChat';
import VoiceControls from '../components/VoiceControls';
import VoiceTutor from '../components/VoiceTutor';

type Concept = { concept: string; explanation: string };
type Card = { question: string; answer: string };
type QuizItem = {
  question: string;
  options: string[];
  correct_answer: string;
  explanation: string;
};

export default function Dashboard(): React.JSX.Element {
  const [summary, setSummary] = useState('');
  const [concepts, setConcepts] = useState<Concept[]>([]);
  const [cards, setCards] = useState<Card[]>([]);
  const [quiz, setQuiz] = useState<QuizItem[]>([]);
  const [voiceSpeed, setVoiceSpeed] = useState(1);
  const [voiceExplanation, setVoiceExplanation] = useState('');
  const [explanationText, setExplanationText] = useState('');
  const [darkMode, setDarkMode] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [activeSection, setActiveSection] = useState('upload');

  useEffect(() => {
    const root = document.documentElement;
    if (darkMode) root.classList.add('dark');
    else root.classList.remove('dark');
  }, [darkMode]);

  const navigateToSection = (id: string) => {
    setActiveSection(id);
    const node = document.getElementById(id);
    if (node) {
      node.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  const refreshGeneratedContent = async (uploadData?: { summary?: string; explanation?: string; voice_explanation?: string }) => {
    const [s, c, f, q, a11y] = await Promise.all([
      api.get('/summary'),
      api.get('/concepts'),
      api.get('/flashcards'),
      api.get('/quiz'),
      api.get('/accessibility'),
    ]);

    setSummary(uploadData?.summary || s.data.summary || '');
    setConcepts(c.data.concepts || []);
    setCards(f.data.flashcards || []);
    setQuiz(q.data.quiz || []);
    setVoiceSpeed(Number(a11y.data.voice_speed || 1));
    setVoiceExplanation(uploadData?.voice_explanation || '');
    setExplanationText(uploadData?.explanation || uploadData?.summary || s.data.summary || '');
  };

  const handleUploaded = async (uploadData: { summary?: string; explanation?: string; voice_explanation?: string }) => {
    await refreshGeneratedContent(uploadData);
    navigateToSection('summary');
  };

  return (
    <Layout
      darkMode={darkMode}
      sidebarCollapsed={sidebarCollapsed}
      activeSection={activeSection}
      onToggleDark={() => setDarkMode((v) => !v)}
      onToggleSidebar={() => setSidebarCollapsed((v) => !v)}
      onNavigate={navigateToSection}
    >
      <PDFUploader onUploaded={handleUploaded} />
      <SummaryViewer summary={summary} />
      <ConceptsViewer concepts={concepts} voiceExplanation={voiceExplanation} fallbackSpeechText={explanationText} />
      <Flashcards cards={cards} />
      <div id="quiz-section">
        <Quiz quiz={quiz} />
      </div>
      <TutorChat />
      <VoiceTutor />
      <VoiceControls defaultText={summary} speed={voiceSpeed} />
      <AccessibilitySettings />
    </Layout>
  );
}
