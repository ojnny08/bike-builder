import { BrowserRouter, Route, Routes } from 'react-router-dom'
import Layout from './components/Layout/Layout'
import ProtectedRoute from './components/ProtextedRoute/ProtectedRoute'
import Login from './pages/LoginPage/Login'
import HomePage from './pages/HomePage/Home'
import Components from './pages/ComponentsPage/Components'
import ComponentDetails from './pages/ComponentsPage/ComponentDetails'
import Builds from './pages/BuildsPage/Builds'
import PublicBuilds from './pages/BuildsPage/PublicBuilds'
import SharedBuild from './pages/BuildsPage/SharedBuild'
import BuildDetail from './pages/BuildsPage/BuildDetail'
import ComponentSelectPage from './pages/BuildsPage/ComponentSelectPage'
import BuildSummary from './pages/BuildsPage/BuildSummary'
import Profile from './pages/ProfilePage/Profile'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<HomePage />} />
          <Route path="/builds/new" element={<Builds />}/>
          <Route path="/builds/new/select/:category" element={<ComponentSelectPage />}/>
          <Route path="/builds/new/select-group/:group/:mode" element={<ComponentSelectPage />}/>
          <Route path="/profile/:username" element={<Profile />}/>
          <Route path="/components" element={<Components />}/>
          <Route path="/components/:id" element={<ComponentDetails />}/>
          <Route path="/builds" element={<PublicBuilds />}/>
          <Route path="/builds/view/:token" element={<BuildDetail />}/>
          <Route path="/builds/shared/:token" element={<SharedBuild />}/>
          <Route element={<ProtectedRoute />}>
            <Route path="/builds/new/review" element={<BuildSummary />}/>

          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
