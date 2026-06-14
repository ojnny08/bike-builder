import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ProtectedRoute from './components/ProtextedRoute/ProtectedRoute'
import Login from './pages/LoginPage/Login'
import HomePage from './pages/HomePage/Home'
import Components from './pages/ComponentsPage/Components'
import Builds from './pages/BuildsPage/Builds'
import PublicBuilds from './pages/BuildsPage/PublicBuilds'
import ComponentSelectPage from './pages/BuildsPage/components/ComponentSelectPage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/components" element={<Components />}/>
          <Route path="/builds/new" element={<Builds />}/>
          <Route path="/builds/new/select/:category" element={<ComponentSelectPage />}/>
          <Route path="/builds" element={<PublicBuilds />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
