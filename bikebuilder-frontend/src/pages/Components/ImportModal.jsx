import { useState, useEffect } from "react";
import { submitProductURL } from "../../services/componentService";
import "../../styles/pages/Components/ImportModal.css";


const ImportModal = ({ onClose, onImported }) => {
    const [url, setUrl] = useState("");
    const [submitting, setSubmitting] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        const onKey = (e) => e.key === "Escape" && onClose();
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, [onClose]);

    const submit = async (e) => {
        e.preventDefault();
        if (!url.trim() || submitting) return;
        setSubmitting(true);
        setError("");
        try {
            await submitProductURL(url.trim());
            onImported?.();
            onClose();
        } catch (err) {
            const detail = err.response?.data;
            setError(detail?.url?.[0] || detail?.detail || "Could not import that link.");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div className="modal-overlay" onMouseDown={onClose}>
            <div
                className="modal"
                role="dialog"
                aria-modal="true"
                aria-labelledby="import-title"
                onMouseDown={e => e.stopPropagation()}
            >
                <button type="button" className="modal-close" onClick={onClose} aria-label="Close">×</button>
                <h2 id="import-title" className="modal-title">Import a component URL</h2>
                <p className="modal-subtitle">Paste a product link from an approved retailer.</p>

                <form onSubmit={submit} className="modal-form">
                    <input
                        type="url"
                        className="filter-input"
                        placeholder="https://..."
                        value={url}
                        onChange={e => setUrl(e.target.value)}
                        autoFocus
                    />
                    {error && <p className="modal-error">{error}</p>}
                    <div className="modal-actions">
                        <button type="button" className="filter-clear" onClick={onClose}>Cancel</button>
                        <button type="submit" className="modal-submit" disabled={submitting || !url.trim()}>
                            {submitting ? "Importing…" : "Import"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
};

export default ImportModal;
