import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtextedRoute/ProtectedRoute'
import Login from './pages/LoginPage/Login'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<div>Home</div>} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
