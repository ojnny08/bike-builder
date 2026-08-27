import { BrowserRouter, Route, Routes } from 'react-router-dom'
import ScrollToTop from './components/ScrollToTop'
import Layout from './components/Layout/Layout'
import Home from './pages/Home/Home'
import Components from './pages/Components/Components'
import ComponentDetails from './pages/Components/ComponentDetails'
import Builds from './pages/Builds/Builds'
import PublicBuilds from './pages/Builds/PublicBuilds'
import SharedBuild from './pages/Builds/SharedBuild'
import BuildDetail from './pages/Builds/BuildDetail'
import BuildSummary from './pages/Builds/BuildSummary'
import Profile from './pages/Profile/Profile'

function App() {
  return (
    <BrowserRouter>
      <ScrollToTop />
      <Routes>
        <Route element={<Layout />}>
          <Route path="/" element={<Home />} />
          <Route path="/builds/new" element={<Builds />}/>
          <Route path="/profile/:username" element={<Profile />}/>
          <Route path="/components" element={<Components />}/>
          <Route path="/components/:id" element={<ComponentDetails />}/>
          <Route path="/builds" element={<PublicBuilds />}/>
          <Route path="/builds/view/:token" element={<BuildDetail />}/>
          <Route path="/builds/shared/:token" element={<SharedBuild />}/>
          <Route path="/builds/new/review" element={<BuildSummary />}/>
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
