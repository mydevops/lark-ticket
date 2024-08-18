import { createRoot } from 'react-dom/client';
import App from './App.tsx';
import { HashRouter } from 'react-router-dom';
import './style/globals.css';

createRoot(document.getElementById('root')!).render(
  <HashRouter basename="/">
    <App />
  </HashRouter>,
);
