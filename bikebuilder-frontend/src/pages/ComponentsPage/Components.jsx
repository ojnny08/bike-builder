import { useState, useEffect } from "react";
import { fetchComponentsByCategory } from "../../services/componentService";
import "./Components.css";

const COMPONENT_TYPES = [
    { value: "frame",            label: "Frame" },
    { value: "fork",             label: "Fork" },
    { value: "bottom_bracket",   label: "Bottom Bracket" },
    { value: "crankset",         label: "Crankset" },
    { value: "cassette",         label: "Cassette" },
    { value: "rear_derailleur",  label: "Rear Derailleur" },
    { value: "front_derailleur", label: "Front Derailleur" },
    { value: "wheel",            label: "Wheel" },
    { value: "tire",             label: "Tire" },
    { value: "handlebar",        label: "Handlebar" },
    { value: "stem",             label: "Stem" },
    { value: "brake",            label: "Brake" },
    { value: "saddle",           label: "Saddle" },
    { value: "seatpost",         label: "Seatpost" },
];

const Components = () => {
    const [selectedType, setSelectedType] = useState(null);
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!selectedType) return;
        setLoading(true);
        fetchComponentsByCategory(selectedType)
            .then(data => setComponents(data))
            .catch(err => console.log(err))
            .finally(() => setLoading(false));
    }, [selectedType]);

    if (!selectedType) {
        return (
            <div className="components-page">
                <h2 className="components-title">Products</h2>
                <p className="components-subtitle">Select a component type to browse.</p>
                <div className="component-type-grid">
                    {COMPONENT_TYPES.map(type => (
                        <button
                            key={type.value}
                            className="component-type-card"
                            onClick={() => setSelectedType(type.value)}
                        >
                            {type.label}
                        </button>
                    ))}
                </div>
            </div>
        );
    }

    const activeLabel = COMPONENT_TYPES.find(t => t.value === selectedType)?.label;

    return (
        <div className="components-page">
            <div className="components-header">
                <div>
                    <h2 className="components-title">{activeLabel}</h2>
                    <p className="components-subtitle">{components.length} products</p>
                </div>
                <button className="back-btn" onClick={() => setSelectedType(null)}>
                    ← All Categories
                </button>
            </div>

            {loading ? (
                <p className="loading-text">Loading...</p>
            ) : components.length === 0 ? (
                <p className="loading-text">No components found.</p>
            ) : (
                <div className="product-grid">
                    {components.map(comp => (
                        <div key={comp.id} className="product-card">
                            <div className="product-card-body">
                                <p className="product-brand">{comp.brand}</p>
                                <h3 className="product-name">{comp.name}</h3>
                                {comp.description && (
                                    <p className="product-desc">{comp.description}</p>
                                )}
                            </div>
                            <div className="product-card-footer">
                                <span className="product-price">${comp.price}</span>
                                <span className="product-weight">{comp.weight_grams}g</span>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default Components;
