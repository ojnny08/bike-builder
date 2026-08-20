import { Outlet } from 'react-router-dom'
import NavBar from '../NavBar/NavBar'
import './Layout.css'

const Layout = () => {
    return (
        <div>
            <NavBar />
            <Outlet />
        </div>
    );
};

export default Layout;
