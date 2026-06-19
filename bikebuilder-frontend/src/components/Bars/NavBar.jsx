import { useEffect, useRef, useState } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { fetchCurrentUserProfile } from "../../services/userService";
import "./NavBar.css";

const NavBar = () => {
    const { currentUser, logout } = useAuth();
    const [profileUsername, setProfileUsername] = useState(null);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!currentUser) return;
        fetchCurrentUserProfile().then(data => setProfileUsername(data.username));
    }, [currentUser]);

    useEffect(() => {
        const handleClickOutside = (e) => {
            if (dropdownRef.current && !dropdownRef.current.contains(e.target))
                setDropdownOpen(false);
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
    }, []);

    return (
        <nav className="navbar">
            <div className="navbar-top">
                <NavLink to="/" className="navbar-brand">
                    <span className="navbar-brand-icon">&#x1F6B4;</span>
                    Bikco
                </NavLink>
                <div className="navbar-auth">
                    {currentUser ? (
                        <div className="navbar-user" ref={dropdownRef}>
                            <div className="navbar-user-info" onClick={() => profileUsername && navigate(`/profile/${profileUsername}`)}>
                                {currentUser.photoURL
                                    ? <img src={currentUser.photoURL} alt={currentUser.displayName} className="navbar-avatar" />
                                    : <div className="navbar-avatar-placeholder">{currentUser.displayName?.[0] ?? "?"}</div>
                                }
                                <span className="navbar-username">{currentUser.displayName}</span>
                            </div>
                            <button className="navbar-chevron" onClick={() => setDropdownOpen(prev => !prev)}>
                                <span className={`navbar-chevron-icon ${dropdownOpen ? "open" : ""}`} />
                            </button>
                            {dropdownOpen && (
                                <div className="navbar-dropdown">
                                    <button className="navbar-dropdown-item" onClick={() => { logout(); setDropdownOpen(false); }}>
                                        Log Out
                                    </button>
                                </div>
                            )}
                        </div>
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
