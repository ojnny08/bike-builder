import { Outlet } from 'react-router-dom'
import NavBar from '../Bars/NavBar'
import './Layout.css'

const Layout = () => (
    <div>
        <NavBar />
        <main className="page-wrapper">
            <Outlet />
        </main>
    </div>
);

export default Layout;
