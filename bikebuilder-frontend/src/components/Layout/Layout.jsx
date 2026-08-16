import { Outlet, useLocation } from 'react-router-dom'
import NavBar from '../NavBar/NavBar'
import { useBuild } from '../../context/BuildContext'
import './Layout.css'

const Layout = () => {
    const location = useLocation();
    const { build } = useBuild();

    // Once a bike type is chosen the builder takes over the whole screen with
    // its own top bar, so the site navbar is hidden across the builder flow.
    const inBuilder = location.pathname.startsWith('/builds/new') && build.bikeType;

    return (
        <div>
            {!inBuilder && <NavBar />}
            <Outlet />
        </div>
    );
};

export default Layout;
