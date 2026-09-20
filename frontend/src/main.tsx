import React from 'react';
import ReactDOM from 'react-dom/client';
import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import Home from './pages/Home';
import InsightsHistory from './pages/InsightsHistory';
import Intro from './pages/Intro';
import LearningExperience from './pages/LearningExperience';
import Mindset from './pages/Mindset';
import Profile from './pages/Profile';
import Roadmap from './pages/Roadmap';
import SignIn from './pages/SignIn';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';

import './styles.css';

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <a href="#main" className="sr-only focus:not-sr-only">Skip to main content</a>
  <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Navigate to="/intro" replace />} />
          <Route path="/intro" element={<Intro />} />
          <Route path="/signin" element={<SignIn />} />
          
          <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
          <Route path="/mindset" element={<ProtectedRoute><Mindset /></ProtectedRoute>} />
          
          <Route path="/home" element={<ProtectedRoute requireOnboarding><Home /></ProtectedRoute>} />
          <Route path="/roadmap/:sessionId" element={<ProtectedRoute requireOnboarding><Roadmap /></ProtectedRoute>} />
          <Route path="/learning/:roadmapId/:nodeId" element={<ProtectedRoute requireOnboarding><LearningExperience /></ProtectedRoute>} />
          <Route path="/insights" element={<ProtectedRoute requireOnboarding><InsightsHistory /></ProtectedRoute>} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  </React.StrictMode>
);
