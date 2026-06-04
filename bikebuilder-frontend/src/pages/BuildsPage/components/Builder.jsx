import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../../api/axios";
import { useBuild } from "../../../context/BuildContext";
import ProgressBar from "./ProgressBar";
import "../Builds.css";

const fmt = str => str.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

const Builder = () => {
    const { build, emptyBuild, addComponent } = useBuild();
    const [name, setName] = useState("");
    const [currentStep, setCurrentStep] = useState(0);
    const [components, setComponents] = useState([]);
    const [loadingComponents, setLoadingComponents] = useState(false);
    const [saving, setSaving] = useState(false);
    const navigate = useNavigate();

    const { required = [], optional = [] } = build.bikeType.rules ?? {};
    const allCategories = [...required, ...optional];
    const activeCategory = allCategories[currentStep];
    const isLastStep = currentStep === allCategories.length - 1;

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    useEffect(() => {
        if (!activeCategory) return;
        setLoadingComponents(true);
        api.get("/api/components/components/", { params: { category: activeCategory } })
            .then(res => setComponents(res.data))
            .finally(() => setLoadingComponents(false));
    }, [activeCategory]);

    const handleNext = () => {
        if (!isLastStep) setCurrentStep(s => s + 1);
    };

    const handleBack = () => {
        if (currentStep > 0) setCurrentStep(s => s - 1);
    };

    const handleSaveBuild = async () => {
        setSaving(true);
        const selectedTypes = new Set(build.components.map(c => c.component_type));
        const allRequiredFilled = required.every(t => selectedTypes.has(t));
        try {
            await api.post("/api/builds/build/", {
                name: name || `${build.bikeType.name} Build`,
                bikeType: build.bikeType.id,
                components: build.components.map(c => c.id),
                status: allRequiredFilled ? "complete" : "in_progress",
            });
            navigate("/builds-all");
        } finally {
            setSaving(false);
            emptyBuild();
        }
    };

    return (
        <div className="builder-wrapper">
            <ProgressBar
                steps={allCategories}
                currentStep={currentStep}
                selectedByCategory={selectedByCategory}
                onStepClick={setCurrentStep}
            />
            <div className="progress-bar-spacer" />

            <div className="builds-page">
                <div className="builder-header">
                    <div>
                        <h2 className="builds-title">{fmt(activeCategory)}</h2>
                        <span className="progress-text">Step {currentStep + 1} of {allCategories.length}</span>
                    </div>
                    <div className="builder-actions">
                        <input
                            className="build-name-input"
                            type="text"
                            placeholder="Name your build..."
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                        <button className="start-over-btn" onClick={emptyBuild}>Start Over</button>
                    </div>
                </div>

                <div className="step-layout">
                    <section className="component-panel">
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
                                        <span className="summary-category">{fmt(c.component_type)}</span>
                                        <span className="summary-name">{c.name}</span>
                                    </li>
                                ))}
                            </ul>
                        )}
                    </aside>
                </div>

                {/* Step navigation */}
                <div className="step-nav">
                    <button className="step-back-btn" onClick={handleBack} disabled={currentStep === 0}>Back</button>
                    {isLastStep ? (
                        <button className="save-build-btn" onClick={handleSaveBuild} disabled={saving}>
                            {saving ? "Saving..." : "Save Build"}
                        </button>
                    ) : (
                        <button className="step-next-btn" onClick={handleNext}>Next</button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Builder;
