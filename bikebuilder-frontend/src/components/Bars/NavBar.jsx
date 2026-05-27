import { NavLink } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {

    return (
        <nav className="navbar">
            <span className="navbar-brand">BikeBuilder</span>
            <div className="navbar-links">
                <NavLink to="/">Home</NavLink>
                <NavLink to="/components">Components</NavLink>
                <NavLink to="/builds">Builds</NavLink>
            </div>
        </nav>
    )
}

export default NavBar;