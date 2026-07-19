import { Outlet, useLocation } from 'react-router-dom'
import NavBar from '../Bars/NavBar'
import { useBuild } from '../../context/BuildContext'
import './Layout.css'

const Layout = () => {
    const location = useLocation();
    const { build } = useBuild();

    // Once a bike type is chosen the builder takes over the whole screen with
    // its own top bar, so the site navbar is hidden across the builder flow.
    const inBuilder = location.pathname.startsWith('/builds/new') && build.bikeType;
    const isHome = location.pathname === "/";

    const wrapperClass = inBuilder
        ? "page-wrapper"
        : isHome
            ? "page-wrapper page-wrapper--home"
            : "page-wrapper page-wrapper--with-nav";

    return (
        <div>
            {!inBuilder && <NavBar />}
            <main className={wrapperClass}>
                <Outlet />
            </main>
        </div>
    );
};

export default Layout;
