import { createUserWithEmailAndPassword, GoogleAuthProvider, linkWithCredential, signInWithEmailAndPassword, signInWithPopup, signOut, validatePassword } from "firebase/auth"
import { googleProvider, auth } from "../../api/firebase"
import { fetchCurrentUserProfile } from "../../services/userService";
import { useEffect, useState } from "react";
import { createPortal } from "react-dom";
import "../../styles/components/Auth/AuthPopUp.css";

const passwordPolicyCheck = (status) => {
    if (status.isValid) return [];
    const missing = [];
    if (status.meetsMinPasswordLength === false) missing.push("more characters");
    if (status.containsLowercaseLetter === false) missing.push("a lowercase letter");
    if (status.containsUppercaseLetter === false) missing.push("an uppercase letter");
    if (status.containsNumericCharacter === false) missing.push("a number");
    if (status.containsNonAlphanumericCharacter === false) missing.push("a symbol");
    return missing;
};

const authErrorMessage = (err) => {
    const response = err.cause?.response;
    if (response) {
        const detail = response.data?.detail;
        if ((response.status === 401 || response.status === 403) && detail) return detail;
        return "We could not load your account. Please try again.";
    }
    if (err.code === "auth/email-already-in-use") return "An account with this email already exists.";
    if (err.code === "auth/weak-password") return "Password must be at least 6 characters.";
    return "Invalid email or password.";
};

const AuthPopUp = ({ onSelect, isSignUp }) => {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [register, setRegister] = useState(isSignUp);
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [passwordNotice, setPasswordNotice] = useState([]);
    const [pendingCredential, setPendingCredential] = useState(null);

    const close = () => {
        setPendingCredential(null);
        onSelect?.(false);
    };

    const loadProfileOrSignOut = async () => {
        try {
            await fetchCurrentUserProfile();
        } catch (err) {
            await signOut(auth);
            throw err;
        }
    };

    useEffect(() => {
        if (!register || !password) return;
        let cancelled = false;
        validatePassword(auth, password)
            .then((status) => { if (!cancelled) setPasswordNotice(passwordPolicyCheck(status)); })
            .catch(() => { if (!cancelled) setPasswordNotice([]); });
        return () => { cancelled = true; };
    }, [password, register]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");

        if (pendingCredential) {
            setSubmitting(true);
            try {
                const { user } = await signInWithEmailAndPassword(auth, email, password);
                await linkWithCredential(user, pendingCredential);
                setPendingCredential(null);
                await loadProfileOrSignOut();
                close();
            } catch (err) {
                setError(err.cause?.response
                    ? authErrorMessage(err)
                    : "That password is not correct. Try again to connect Google.");
            } finally {
                setSubmitting(false);
            }
            return;
        }

        if (register && password !== confirmPassword) return setError("Passwords do not match")
        setSubmitting(true);
        try {
            if (register) {
                await createUserWithEmailAndPassword(auth, email, password);
            } else {
                await signInWithEmailAndPassword(auth, email, password);
            }
            await loadProfileOrSignOut();
            close();
        } catch (err) {
            setError(authErrorMessage(err));
        } finally {
            setSubmitting(false);
        }
    }

    const handleGoogleLogin = async () => {
        setError("");
        try {
            await signInWithPopup(auth, googleProvider);
            await loadProfileOrSignOut();
            close();
        } catch (err) {
            if (err.code === "auth/account-exists-with-different-credential") {
                setPendingCredential(GoogleAuthProvider.credentialFromError(err));
                setEmail(err.customData?.email ?? "");
                setPassword("");
                setError("This email already has an account. Enter your password to connect Google.");
                return;
            }
            if (err.cause?.response) return setError(authErrorMessage(err));
            await signOut(auth);
            setError("Google sign-in failed");
        }
    }

    return createPortal(
        <div className="auth-modal-overlay" onClick={close}>
            <div className="auth-modal" onClick={(e) => e.stopPropagation()}>
                <button className="auth-modal-close" onClick={close} aria-label="Close">×</button>

                <h2 className="auth-modal-title">
                    {pendingCredential ? "Connect Google" : "Welcome to Bikco"}
                </h2>
                <p className="auth-modal-subtitle">
                    {pendingCredential
                        ? "You already signed up with this email. Enter your password once and Google will work from now on."
                        : register ? "Join Bikco for free to show off your bikes" : "Log in to explore more"}
                </p>

                {error && <div className="auth-error">{error}</div>}

                <form className="auth-form" onSubmit={handleSubmit}>
                    <input
                        type="email"
                        value={email}
                        placeholder="Email"
                        onChange={(e) => setEmail(e.target.value)}
                        readOnly={Boolean(pendingCredential)}
                        required
                    />
                    <input
                        type="password"
                        value={password}
                        placeholder="Password"
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    {!pendingCredential && register && password && passwordNotice.length > 0 && (
                        <ul className="auth-notice">
                            {passwordNotice.map((m) => <li key={m}>{m}</li>)}
                        </ul>
                    )}
                    {!pendingCredential && register && (
                        <input
                            type="password"
                            value={confirmPassword}
                            placeholder="Confirm Password"
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required/>
                    ) }
                    <button className="auth-submit" type="submit" disabled={submitting}>
                        {pendingCredential ? "Connect Google" : register ? "Sign up" : "Log in"}
                    </button>
                </form>

                {!pendingCredential && <>
                <div className="auth-divider">or</div>

                <button className="auth-google" onClick={handleGoogleLogin}>
                    <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                    Continue with Google
                </button>

                <p className="auth-switch">
                    {register ? "Already have an account? " : "Dont have an account? "}
                    <button
                        className="auth-toggle"
                        onClick={() => { setRegister(!register); setError(""); setConfirmPassword(""); }}
                    >
                        {register ? "Log in" : "Sign up"}
                    </button>
                </p>
                </>}
            </div>
        </div>,
        document.body
    )
}

export default AuthPopUp;
