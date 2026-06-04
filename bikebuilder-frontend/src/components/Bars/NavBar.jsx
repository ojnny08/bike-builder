import { NavLink } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./NavBar.css";

const NavBar = () => {

    const { logout } = useAuth();


    return (
        <nav className="navbar">
            <span className="navbar-brand">BikeBuilder</span>
            <div className="navbar-links">
                <NavLink to="/">Home</NavLink>
                <NavLink to="/components">Components</NavLink>
                <NavLink to="/builds">Builds</NavLink>
                <NavLink to="/builds-all">Public Builds</NavLink>
                <button onClick={logout}>Logout</button>
            </div>
        </nav>
    )
}

export default NavBar;