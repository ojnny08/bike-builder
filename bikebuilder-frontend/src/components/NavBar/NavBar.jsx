import { useEffect, useRef, useState } from "react";
import { NavLink, Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";
import { fetchCurrentUserProfile } from "../../services/userService";
import "../../styles/components/NavBar/NavBar.css";
import AuthPopUp from "../Auth/AuthPopUp";

const NavBar = () => {
    const { currentUser, logout } = useAuth();
    const [profileUsername, setProfileUsername] = useState(null);
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const [authMode, setAuthMode] = useState(null);
    const [imgFailed, setImgFailed] = useState(false);
    const dropdownRef = useRef(null);
    const navigate = useNavigate();

    useEffect(() => {
        if (!currentUser) return;
        setImgFailed(false);
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
        <nav className="nav">
            <div className="nav-top">
                <div className="nav-left">
                    <NavLink to="/" className="nav-brand">
                        <svg className="nav-brand-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                            <circle cx="18.5" cy="17.5" r="3.5" />
                            <circle cx="5.5" cy="17.5" r="3.5" />
                            <circle cx="15" cy="5" r="1" />
                            <path d="M12 17.5V14l-3-3 4-3 2 3h2" />
                        </svg>
                        Bikco
                    </NavLink>
                    <div className="nav-links">
                        <NavLink to="/">Home</NavLink>
                        <NavLink to="/builds/new">Builder</NavLink>
                        <NavLink to="/components">Products</NavLink>
                        <NavLink to="/builds" end>Completed Bikes</NavLink>
                    </div>
                </div>
                <div className="nav-auth">
                    {currentUser ? (
                        <div className="nav-user" ref={dropdownRef}>
                            <div className="nav-user-info" onClick={() => profileUsername && navigate(`/profile/${profileUsername}`)}>
                                {currentUser.photoURL && !imgFailed
                                    ? <img src={currentUser.photoURL} className="nav-avatar" referrerPolicy="no-referrer" onError={() => setImgFailed(true)} />
                                    : <div className="nav-avatar-fallback">{currentUser.displayName?.[0] ?? "?"}</div>
                                }

                            </div>
                            <button className="nav-chevron" onClick={() => setDropdownOpen(prev => !prev)}>
                                <span className={`nav-chevron-icon${dropdownOpen ? " is-open" : ""}`} />
                            </button>
                            {dropdownOpen && (
                                <div className="nav-dropdown">
                                    <button className="nav-dropdown-item" onClick={() => { logout(); setDropdownOpen(false); }}>
                                        Log Out
                                    </button>
                                </div>
                            )}
                        </div>
                    ) : (
                        <>
                            <button onClick={() => setAuthMode("login")} className="nav-auth-link">Log In</button>
                            <div className="nav-auth-link">|</div>
                            <button onClick={() => setAuthMode("signup")} className="nav-auth-link">Sign Up</button>
                            {authMode && (
                                <AuthPopUp onSelect={() => setAuthMode(null)} isSignUp={authMode === "signup"}/>
                            )}
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default NavBar;
