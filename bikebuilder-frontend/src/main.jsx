import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { BuildProvider } from './context/BuildContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <BuildProvider>
        <App />
      </BuildProvider>
    </AuthProvider>
  </StrictMode>,
)
