import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ScrollToTop from './components/ScrollToTop'
import Layout from './components/Layout/Layout'
import ProtectedRoute from './components/ProtextedRoute/ProtectedRoute'
import Login from './pages/Login/Login'
import Home from './pages/Home/Home'
import Components from './pages/Components/Components'
import ComponentDetails from './pages/Components/ComponentDetails'
import Builds from './pages/Builds/Builds'
import PublicBuilds from './pages/Builds/PublicBuilds'
import SharedBuild from './pages/Builds/SharedBuild'
import BuildDetail from './pages/Builds/BuildDetail'
import ComponentSelect from './pages/Builds/ComponentSelect'
import BuildSummary from './pages/Builds/BuildSummary'
import Profile from './pages/Profile/Profile'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/builds/new" element={<Builds />}/>
          <Route path="/builds/new/select/:category" element={<ComponentSelect />}/>
          <Route path="/builds/new/select-group/:group/:mode" element={<ComponentSelect />}/>
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
