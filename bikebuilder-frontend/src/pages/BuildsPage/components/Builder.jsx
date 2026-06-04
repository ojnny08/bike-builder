import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../../api/axios";
import { useBuild } from "../../../context/BuildContext";
import "../Builds.css";

const Builder = () => {
    const { build, emptyBuild, addComponent } = useBuild();
    const [name, setName] = useState("");
    const [activeCategory, setActiveCategory] = useState(build.bikeType.rules?.required?.[0] ?? null);
    const [components, setComponents] = useState([]);
    const [loadingComponents, setLoadingComponents] = useState(false);
    const [saving, setSaving] = useState(false);
    const [saved, setSaved] = useState(false);
    const navigate = useNavigate();

    useEffect(() => {
        if (!activeCategory) return;
        setLoadingComponents(true);
        api.get("/api/components/components/", { params: { category: activeCategory } })
            .then(res => setComponents(res.data))
            .finally(() => setLoadingComponents(false));
    }, [activeCategory]);

    const handleSaveBuild = async () => {
        setSaving(true);
        const requiredTypes = build.bikeType.rules?.required ?? [];
        const selectedTypes = new Set(build.components.map(c => c.component_type));
        const allRequiredFilled = requiredTypes.every(t => selectedTypes.has(t));
        try {
            await api.post("/api/builds/build/", {
                name: name || `${build.bikeType.name} Build`,
                bikeType: build.bikeType.id,
                components: build.components.map(c => c.id),
                status: allRequiredFilled ? "complete" : "in_progress",
            });
            setSaved(true);
            navigate("/builds-all");
        } finally {
            setSaving(false);
            emptyBuild();
        }
    };

    const { required = [], optional = [] } = build.bikeType.rules ?? {};
    const allCategories = [...required, ...optional];
    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );
    const filledRequired = required.filter(t => selectedByCategory[t]).length;

    return (
        <div className="builds-page">
            <div className="builder-header">
                <div>
                    <h2 className="builds-title">{build.bikeType.name} Build</h2>
                    <input
                        className="build-name-input"
                        type="text"
                        placeholder="Name your build..."
                        value={name}
                        onChange={e => setName(e.target.value)}
                    />
                    <span className="progress-text">
                        {filledRequired} / {required.length} required components selected
                    </span>
                </div>
                <div className="builder-actions">
                    <button className="start-over-btn" onClick={emptyBuild}>Start Over</button>
                    <button className="save-build-btn" onClick={handleSaveBuild} disabled={saving || saved}>
                        {saved ? "Saved!" : saving ? "Saving..." : "Save Build"}
                    </button>
                </div>
            </div>

            <div className="builder-layout">
                <aside className="category-sidebar">
                    {allCategories.map(type => {
                        const isFilled = !!selectedByCategory[type];
                        const isActive = activeCategory === type;
                        const isRequired = required.includes(type);
                        return (
                            <button
                                key={type}
                                className={`category-btn${isActive ? " active" : ""}${isFilled ? " filled" : ""}`}
                                onClick={() => setActiveCategory(type)}
                            >
                                <span className="category-label">{type.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}</span>
                                <span className="category-status">
                                    {isFilled ? "✓" : isRequired ? "required" : "optional"}
                                </span>
                            </button>
                        );
                    })}
                </aside>

                <section className="component-panel">
                    <h3 className="panel-title">{activeCategory?.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase())}</h3>
                    {loadingComponents ? (
                        <p className="loading-text">Loading components...</p>
                    ) : components.length === 0 ? (
                        <p className="empty-state">No components found for this category.</p>
                    ) : (
                        <div className="component-list">
                            {components.map(comp => {
                                const isSelected = selectedByCategory[comp.component_type]?.id === comp.id;
                                return (
                                    <div
                                        key={comp.id}
                                        className={`component-card${isSelected ? " selected" : ""}`}
                                        onClick={() => addComponent(comp)}
                                    >
                                        <div className="component-info">
                                            <h4 className="component-name">{comp.name}</h4>
                                            <p className="component-brand">{comp.brand}</p>
                                        </div>
                                        {isSelected && <span className="selected-badge">Selected</span>}
                                    </div>
                                );
                            })}
                        </div>
                    )}
                </section>

                <aside className="build-summary">
                    <h3 className="summary-title">Your Build</h3>
                    {build.components.length === 0 ? (
                        <p className="empty-state">Select components to build your bike.</p>
                    ) : (
                        <ul className="summary-list">
                            {build.components.map(c => (
                                <li key={c.id} className="summary-item">
                                    <span className="summary-category">{c.component_type}</span>
                                    <span className="summary-name">{c.name}</span>
                                </li>
                            ))}
                        </ul>
                    )}
                </aside>
            </div>
        </div>
    );
};

export default Builder;
