import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './styles/index.css'
import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'
import { BuildProvider } from './context/BuildContext.jsx'
import { AuthPopUpProvider } from './context/AuthPopUpContext.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <AuthProvider>
      <BuildProvider>
        <AuthPopUpProvider>
          <App />
        </AuthPopUpProvider>
      </BuildProvider>
    </AuthProvider>
  </StrictMode>,
)
