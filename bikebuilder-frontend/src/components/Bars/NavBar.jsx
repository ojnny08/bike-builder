import { NavLink, Link } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import "./NavBar.css";

const NavBar = () => {
    const { currentUser, logout } = useAuth();

    return (
        <nav className="navbar">
            <div className="navbar-top">
                <NavLink to="/" className="navbar-brand">
                    <span className="navbar-brand-icon">&#x1F6B4;</span>
                    BUILD A BIKE
                </NavLink>
                <div className="navbar-auth">
                    {currentUser ? (
                        <button className="navbar-auth-btn" onClick={logout}>Log Out</button>
                    ) : (
                        <>
                            <Link to="/login" className="navbar-auth-link">Log In</Link>
                            <span className="navbar-auth-sep">|</span>
                            <Link to="/signup" className="navbar-auth-link">Sign Up</Link>
                        </>
                    )}
                </div>
            </div>
            <div className="navbar-links">
                <NavLink to="/builds/new">Bike Builder</NavLink>
                <NavLink to="/components">Products</NavLink>
                <NavLink to="/builds" end>Completed Builds</NavLink>
            </div>
        </nav>
    );
};

export default NavBar;
