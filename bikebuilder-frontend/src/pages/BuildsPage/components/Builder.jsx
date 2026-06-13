import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import "../Builds.css";
import { createBuild, updateBuild } from "../../../services/buildService";
import { fetchComponentsByCategory, fetchCompatibleComponents } from "../../../services/componentService";


const UPSTREAM_DEPS = {
    bottom_bracket: 'frame',
    crankset: 'bottom_bracket',
    cassette: 'crankset',
    rear_derailleur: 'cassette',
    front_derailleur: 'crankset',
    wheel: 'frame',
    tire: 'wheel',
};

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

const Builder = () => {
    const { build, emptyBuild, addComponent } = useBuild();
    const { required = [], optional = [] } = build.bikeType.rules;
    const allCategories = [...required, ...optional];
    const [name, setName] = useState(build.name || "");
    const [activeCategory, setActiveCategory] = useState(null);
    const [components, setComponents] = useState([]);
    const [loadingComponents, setLoadingComponents] = useState(false);
    const [saving, setSaving] = useState(false);
    const navigate = useNavigate();

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const componentKey = build.components.map(c => c.id).join(',');

    const isLocked = (cat) => {
        const dep = UPSTREAM_DEPS[cat];
        return dep && allCategories.includes(dep) && !selectedByCategory[dep];
    };

    useEffect(() => {
        if (!activeCategory) return;
        const load = async () => {
            setLoadingComponents(true);
            try {
                const selectedIds = Object.fromEntries(
                    allCategories
                        .slice(0, allCategories.indexOf(activeCategory))
                        .filter(t => selectedByCategory[t])
                        .map(t => [`${t}_id`, selectedByCategory[t].id])
                );
                const [all, compatible] = await Promise.all([
                    fetchComponentsByCategory(activeCategory),
                    activeCategory === 'frame'
                        ? Promise.resolve(null)
                        : fetchCompatibleComponents(activeCategory, selectedIds),
                ]);
                const compatibleIds = new Set((compatible ?? all).map(c => c.id));
                setComponents(all.map(c => ({ ...c, compatible: compatibleIds.has(c.id) })));
            } catch (e) {
                console.error(e);
            } finally {
                setLoadingComponents(false);
            }
        };
        load();
    }, [activeCategory, componentKey]);

    const handleSaveBuild = async () => {
        setSaving(true);
        const selectedTypes = new Set(build.components.map(c => c.component_type));
        const allRequiredFilled = required.every(t => selectedTypes.has(t));
        const payload = {
            name: name || `${build.bikeType.name} Build`,
            bikeType: build.bikeType.id,
            components: build.components.map(c => c.id),
            status: allRequiredFilled ? "complete" : "in_progress",
        };
        try {
            if (build.id) await updateBuild(build.id, payload);
            else await createBuild(payload);
            navigate("/builds");
        } finally {
            setSaving(false);
            emptyBuild();
        }
    };

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight) || 0), 0);

    return (
        <div className="pcp-wrapper">
            <div className="pcp-main">
                {/* Top bar */}
                <div className="pcp-topbar">
                    <div className="pcp-topbar-left">
                        <span className="pcp-build-type">{build.bikeType.name}</span>
                        <input
                            className="pcp-name-input"
                            type="text"
                            placeholder="Name your build..."
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                    </div>
                    <div className="pcp-topbar-right">
                        <button className="pcp-start-over" onClick={emptyBuild}>Start Over</button>
                        <button className="pcp-save-btn" onClick={handleSaveBuild} disabled={saving}>
                            {saving ? "Saving..." : "Save Build"}
                        </button>
                    </div>
                </div>

                {/* Component rows */}
                <div className="pcp-list">
                    {allCategories.map(cat => {
                        const selected = selectedByCategory[cat];
                        const locked = isLocked(cat);
                        const isActive = activeCategory === cat;

                        return (
                            <div key={cat} className="pcp-item-wrap">
                                <div
                                    className={`pcp-item${isActive ? ' pcp-item-active' : ''}${locked ? ' pcp-item-locked' : ''}`}
                                    onClick={() => !locked && setActiveCategory(isActive ? null : cat)}
                                >
                                    <span className="pcp-item-cat">{formatCat(cat)}</span>
                                    <div className="pcp-item-center">
                                        {selected ? (
                                            <span className="pcp-item-selected">{selected.name}
                                                <span className="pcp-item-brand"> · {selected.brand}</span>
                                            </span>
                                        ) : locked ? (
                                            <span className="pcp-item-locked-msg">Select prerequisite first</span>
                                        ) : (
                                            <span className="pcp-item-placeholder">Choose {formatCat(cat)}</span>
                                        )}
                                    </div>
                                    <span className="pcp-item-price">
                                        {selected?.price ? `$${parseFloat(selected.price).toFixed(2)}` : '—'}
                                    </span>
                                </div>

                                {isActive && (
                                    <div className="pcp-picker">
                                        {loadingComponents ? (
                                            <p className="loading-text">Loading...</p>
                                        ) : components.length === 0 ? (
                                            <p className="empty-state">No compatible components found.</p>
                                        ) : (
                                            components.map(comp => {
                                                const isSelected = selected?.id === comp.id;
                                                const isCompatible = comp.compatible ?? true;
                                                return (
                                                    <div
                                                        key={comp.id}
                                                        className={`pcp-option${isSelected ? ' pcp-option-selected' : ''}${!isCompatible ? ' pcp-option-incompat' : ''}`}
                                                        onClick={() => {
                                                            if (!isCompatible) return;
                                                            addComponent(comp);
                                                            setActiveCategory(null);
                                                        }}
                                                    >
                                                        <div className="pcp-option-info">
                                                            <span className="pcp-option-name">{comp.name}</span>
                                                            <span className="pcp-option-brand">{comp.brand}</span>
                                                        </div>
                                                        <span className="pcp-option-price">
                                                            {comp.price ? `$${parseFloat(comp.price).toFixed(2)}` : '—'}
                                                        </span>
                                                    </div>
                                                );
                                            })
                                        )}
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Summary panel */}
            <div className="pcp-summary">
                <h3 className="pcp-summary-title">Summary</h3>
                <div className="pcp-summary-list">
                    {allCategories.map(cat => {
                        const comp = selectedByCategory[cat];
                        return (
                            <div key={cat} className="pcp-summary-row">
                                <span className="pcp-summary-cat">{formatCat(cat)}</span>
                                <span className="pcp-summary-val">
                                    {comp ? comp.name : <span className="pcp-summary-empty">—</span>}
                                </span>
                            </div>
                        );
                    })}
                </div>
                <div className="pcp-summary-totals">
                    {totalWeight > 0 && (
                        <div className="pcp-summary-total-row">
                            <span>Total Weight</span>
                            <span>{totalWeight.toFixed(0)}g</span>
                        </div>
                    )}
                    <div className="pcp-summary-total-row pcp-summary-price">
                        <span>Total Price</span>
                        <span>${totalPrice.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Builder;
