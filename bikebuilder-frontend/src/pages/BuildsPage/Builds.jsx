import { useEffect, useState } from "react";
import { useBuild } from "../../context/BuildContext";
import { api } from "../../api/axios";
import "./Builds.css";

const Builds = () => {
    const { build, startNewBuild, updateBuild, addComponent } = useBuild();
    const [bikeTypes, setBikeTypes] = useState([]);
    const [loadingTypes, setLoadingTypes] = useState(true);
    const [activeCategory, setActiveCategory] = useState(null);
    const [components, setComponents] = useState([]);
    const [loadingComponents, setLoadingComponents] = useState(false);

    useEffect(() => {
        api.get("/api/category/bike-types/")
            .then(res => setBikeTypes(res.data))
            .finally(() => setLoadingTypes(false));
    }, []);

    useEffect(() => {
        if (!activeCategory) return;
        setLoadingComponents(true);
        api.get("/api/components/components/", { params: { category: activeCategory } })
            .then(res => setComponents(res.data))
            .finally(() => setLoadingComponents(false));
    }, [activeCategory]);

    const handleSelectBikeType = (bikeType) => {
        updateBuild({ bikeType });
        const firstRule = bikeType.component_rules?.[0];
        if (firstRule) setActiveCategory(firstRule.component_type);
    };

    if (!build.bikeType) {
        return (
            <div className="builds-page">
                <h2 className="builds-title">Choose Your Bike Type</h2>
                <p className="builds-subtitle">Select a frame category to start building your ride.</p>
                {loadingTypes ? (
                    <p className="loading-text">Loading...</p>
                ) : (
                    <div className="bike-type-grid">
                        {bikeTypes.map(bt => (
                            <button
                                key={bt.id}
                                className="bike-type-card"
                                onClick={() => handleSelectBikeType(bt)}
                            >
                                <span className="bike-type-name">{bt.name}</span>
                                <span className="bike-type-count">
                                    {bt.component_rules?.length ?? 0} components
                                </span>
                            </button>
                        ))}
                    </div>
                )}
            </div>
        );
    }

    const rules = build.bikeType.component_rules ?? [];
    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.category, c])
    );
    const requiredCount = rules.filter(r => r.is_required).length;
    const filledRequired = rules.filter(r => r.is_required && selectedByCategory[r.component_type]).length;

    return (
        <div className="builds-page">
            <div className="builder-header">
                <div>
                    <h2 className="builds-title">{build.bikeType.name} Build</h2>
                    <span className="progress-text">
                        {filledRequired} / {requiredCount} required components selected
                    </span>
                </div>
                <button className="start-over-btn" onClick={startNewBuild}>Start Over</button>
            </div>

            <div className="builder-layout">
                <aside className="category-sidebar">
                    {rules.map(rule => {
                        const isFilled = !!selectedByCategory[rule.component_type];
                        const isActive = activeCategory === rule.component_type;
                        return (
                            <button
                                key={rule.component_type}
                                className={`category-btn${isActive ? " active" : ""}${isFilled ? " filled" : ""}`}
                                onClick={() => setActiveCategory(rule.component_type)}
                            >
                                <span className="category-label">{rule.component_type}</span>
                                <span className="category-status">
                                    {isFilled ? "✓" : rule.is_required ? "required" : "optional"}
                                </span>
                            </button>
                        );
                    })}
                </aside>

                <section className="component-panel">
                    <h3 className="panel-title">{activeCategory}</h3>
                    {loadingComponents ? (
                        <p className="loading-text">Loading components...</p>
                    ) : components.length === 0 ? (
                        <p className="empty-state">No components found for this category.</p>
                    ) : (
                        <div className="component-list">
                            {components.map(comp => {
                                const isSelected = selectedByCategory[comp.category]?.id === comp.id;
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
                                        {isSelected && (
                                            <span className="selected-badge">Selected</span>
                                        )}
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
                                    <span className="summary-category">{c.category}</span>
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

export default Builds;
