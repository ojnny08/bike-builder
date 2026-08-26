import { useEffect } from "react";
import ComponentDetailView from "./ComponentDetailView";
import "./ComponentDetailModal.css";

const ComponentDetailModal = ({ id, inBuildFlow, onAdded, onClose }) => {
    useEffect(() => {
        const onKey = (e) => e.key === "Escape" && onClose();
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, [onClose]);

    return (
        <div className="comp-modal-overlay" onMouseDown={onClose}>
            <div
                className="comp-modal"
                role="dialog"
                aria-modal="true"
                onMouseDown={e => e.stopPropagation()}
            >
                <button type="button" className="comp-modal-close" onClick={onClose} aria-label="Close">×</button>
                <ComponentDetailView id={id} inBuildFlow={inBuildFlow} onAdded={onAdded} />
            </div>
        </div>
    );
};

export default ComponentDetailModal;
