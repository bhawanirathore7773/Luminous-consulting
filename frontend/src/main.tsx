import React from 'react';
import { createRoot } from 'react-dom/client';
import './styles/source-design.css';

function App() {
  return (
    <main id="main-content">
      <section style={{maxWidth: '960px', margin: '0 auto', padding: '80px 24px'}}>
        <p style={{letterSpacing: '0.16em', textTransform: 'uppercase'}}>Luminous Consulting</p>
        <h1>SAP Consulting & Transformation</h1>
        <p>The migration shell is ready. Existing page templates, content and design assets remain the source of truth for the final parity implementation.</p>
      </section>
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<React.StrictMode><App /></React.StrictMode>);
