import { useEffect, useState } from "react";
import "../../pages/ComponentsPage/ImportModal.css";
import "./VariantModal.css";
import VariantOptions, { hasVariants } from "./VariantOptions";

const VariantModal = ({ component, onClose, onAdd }) => {
    const options = component.options || [];
    const variantsExist = hasVariants(options);
    const [resolved, setResolved] = useState(null);

    useEffect(() => {
        const onKey = e => e.key === "Escape" && onClose();
        document.addEventListener("keydown", onKey);
        return () => document.removeEventListener("keydown", onKey);
    }, [onClose]);

    const price = resolved ? resolved.price : component.price;
    const displayImage = resolved?.image_colour_url || component.image_url;
    const canAdd = !variantsExist || Boolean(resolved);

    const add = () => {
        if (!canAdd) return;
        onAdd(component, resolved);
        onClose();
    };

    return (
        <div className="modal-overlay" onMouseDown={onClose}>
            <div
                className="modal variant-modal"
                role="dialog"
                aria-modal="true"
                aria-labelledby="variant-title"
                onMouseDown={e => e.stopPropagation()}
            >
                <button type="button" className="modal-close" onClick={onClose} aria-label="Close">×</button>

                <div className="variant-head">
                    {displayImage && (
                        <div className="variant-media">
                            <img src={displayImage} alt={component.name} />
                        </div>
                    )}
                    <div>
                        <p className="variant-brand">{component.brand}</p>
                        <h2 id="variant-title" className="modal-title">{component.name}</h2>
                        <p className="variant-weight">{component.weight_grams}g</p>
                    </div>
                </div>

                {component.description && (
                    <p className="variant-desc">{component.description}</p>
                )}

                <VariantOptions options={options} onResolve={setResolved} />

                <div className="variant-footer">
                    <div className="variant-price">
                        {canAdd ? `$${price}` : "—"}
                    </div>
                    <button type="button" className="modal-submit" onClick={add} disabled={!canAdd}>
                        Add to build
                    </button>
                </div>
            </div>
        </div>
    );
};

export default VariantModal;
