import { useState, useEffect } from "react";
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup } from "firebase/auth";
import { useNavigate } from "react-router-dom";
import { auth, googleProvider } from "../../api/firebase";
import { useAuth } from "../../context/AuthContext";
import { fetchCurrentUser } from "../../services/userService";
import "./Login.css";

const Login = () => {
    const navigate = useNavigate();
    const { currentUser, loading } = useAuth();
    const [isRegister, setIsRegister] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        if (currentUser) navigate('/');
    }, [currentUser]);

    if (loading) return (
        <div>loading</div>
    );

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        try {
            if (isRegister) {
                await createUserWithEmailAndPassword(auth, email, password);
            } else {
                await signInWithEmailAndPassword(auth, email, password);
            }
            await fetchCurrentUser();
        } catch (err) {
            if (err.code === "auth/email-already-in-use") setError("An account with this email already exists.");
            else if (err.code === "auth/weak-password") setError("Password must be at least 6 characters.");
            else setError("Invalid email or password.");
        }
    };

    const handleGoogleLogin = async () => {
        try {
            await signInWithPopup(auth, googleProvider);
            await api.get('/api/users/me/');
        } catch {
            setError("Google sign-in failed");
        }
    };

    return (
        <div className="login-page">
            <div className="login-hero">
                <h1>Welcome to<br />BikeBuilder.</h1>
                <p>Plan, spec, and build your dream bike — all in one place.</p>
            </div>

            <div className="login-form-panel">
                <h2>{isRegister ? "Create account" : "Sign in"}</h2>
                <p className="login-subtitle">
                    {isRegister ? "Already have an account? " : "Don't have an account? "}
                    <button className="btn-toggle" onClick={() => { setIsRegister(!isRegister); setError(""); }}>
                        {isRegister ? "Sign in" : "Register"}
                    </button>
                </p>

                {error && <div className="login-error">{error}</div>}

                <form className="login-form" onSubmit={handleSubmit}>
                    <input
                        type="email"
                        placeholder="Email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                    <input
                        type="password"
                        placeholder="Password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <button className="btn-primary" type="submit">
                        {isRegister ? "Create account" : "Sign in"}
                    </button>
                </form>

                <div className="login-divider">or</div>

                <button className="btn-google" onClick={handleGoogleLogin}>
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                    Continue with Google
                </button>
            </div>
        </div>
    );
};

export default Login;
