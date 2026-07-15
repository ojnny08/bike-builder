import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import BikeCanvas from "../../../threejs/3d-bike/BikeCanvas";
import "../style/Builds.css";

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const money = n => `$${n.toFixed(2)}`;

const ASSEMBLY_ORDER = [
    "frame", "bottom_bracket", "crankset", "chainring", "sprocket",
    "chain", "wheel", "tire", "seatpost", "saddle", "stem", "brake",
    "handlebar", "pedals",
];

const PlusGlyph = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8"
        strokeLinecap="round" aria-hidden="true">
        <path d="M12 5v14M5 12h14" />
    </svg>
);

const ProgressBike = ({ progress }) => (
    <span className="bb-bike" style={{ left: `calc(${progress} * (100% - 40px))` }}>
        <svg className="bb-bike-svg" viewBox="0 0 34 22" fill="none" stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path strokeWidth="1.6" d="M7 15h9M16 15l-3-9M13 6h11M24 6l3 9M13 6L7 15M16 15l8-9M24 6l2.4-2M13 6l-2.4-.4" />
            <circle cx="16" cy="15" r="1.1" strokeWidth="1.3" />
            <g className="bb-wheel">
                <circle cx="7" cy="15" r="5.2" strokeWidth="1.4" />
                <path strokeWidth="0.9" d="M7 9.8v10.4M1.8 15h10.4M3.3 11.3l7.4 7.4M10.7 11.3l-7.4 7.4" />
            </g>
            <g className="bb-wheel">
                <circle cx="27" cy="15" r="5.2" strokeWidth="1.4" />
                <path strokeWidth="0.9" d="M27 9.8v10.4M21.8 15h10.4M23.3 11.3l7.4 7.4M30.7 11.3l-7.4 7.4" />
            </g>
        </svg>
    </span>
);

const PartCard = ({ category, selected, focused, onFocus, onChoose }) => (
    <div
        className={`bs-card${selected ? ' is-filled' : ''}${focused ? ' is-focused' : ''}`}
        role="button"
        tabIndex={0}
        aria-pressed={focused}
        onClick={onFocus}
        onDoubleClick={onChoose}
        onKeyDown={e => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onChoose(); } }}
    >
        <div className="bs-card-main">
            <span className="bs-card-cat">{formatCat(category)}</span>
            {selected ? (
                <span className="bs-card-name">
                    {selected.name}
                    <span className="bs-card-meta"> · {money(parseFloat(selected.price) || 0)}</span>
                </span>
            ) : (
                <span className="bs-card-placeholder">Not selected</span>
            )}
        </div>
        <button
            type="button"
            className="bs-card-add"
            aria-label={`Choose ${formatCat(category).toLowerCase()}`}
            onClick={e => { e.stopPropagation(); onChoose(); }}
        >
            <PlusGlyph />
        </button>
    </div>
);

const BikeStageBuilder = () => {
    const { build, emptyBuild } = useBuild();
    const navigate = useNavigate();
    const [focusedCategory, setFocusedCategory] = useState(null);

    const { required = [], optional = [] } = build.bikeType.rules;

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const allCategories = [...required, ...optional];
    const orderedCats = [
        ...ASSEMBLY_ORDER.filter(c => allCategories.includes(c)),
        ...allCategories.filter(c => !ASSEMBLY_ORDER.includes(c)),
    ];

    const requiredFilled = required.filter(t => selectedByCategory[t]).length;
    const progress = required.length ? requiredFilled / required.length : 0;

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight_grams) || 0), 0);

    const hasComponents = build.components.length > 0;

    const handleStartOver = () => {
        emptyBuild();
        navigate("/builds/new");
    };

    return (
        <div className="bb-wrapper bs-wrapper">
            <header className="bs-topbar">
                <div className="bs-topbar-side">
                    <button className="bb-btn-ghost" onClick={() => navigate(-1)}>← Back</button>
                    <button className="bb-btn-ghost" onClick={() => navigate("/")}>Home</button>
                </div>
                <span className="bs-topbar-title">Builder</span>
                <div className="bs-topbar-side bs-topbar-side-end">
                    <button className="bb-btn-ghost" onClick={handleStartOver}>Start over</button>
                    <button
                        className="bb-btn-primary"
                        onClick={() => navigate("/builds/new/review")}
                        disabled={!hasComponents}
                    >
                        Save progress
                    </button>
                </div>
            </header>

            <div className="bs-brandrow">
                <div className="bb-progress" aria-label={`${requiredFilled} of ${required.length} essential parts selected`}>
                    <ProgressBike progress={progress} />
                    <span className="bb-bar-track">
                        <span className="bb-bar-fill" style={{ transform: `scaleX(${progress})` }} />
                    </span>
                </div>
            </div>

            <div className="bs-stage-layout">
                <div className="bs-canvas">
                    <BikeCanvas />
                    <div className="bs-canvas-hint">
                        <span className="bs-canvas-title">3D preview</span>
                        <span className="bs-canvas-sub">
                            {focusedCategory ? `Focused · ${formatCat(focusedCategory)}` : "Select a part to focus the view"}
                        </span>
                    </div>
                </div>

                <aside className="bs-panel">
                    <div className="bs-panel-list">
                        {orderedCats.map(category => (
                            <PartCard
                                key={category}
                                category={category}
                                selected={selectedByCategory[category]}
                                focused={focusedCategory === category}
                                onFocus={() => setFocusedCategory(category)}
                                onChoose={() => navigate(`/builds/new/select/${category}`)}
                            />
                        ))}
                    </div>

                    <div className="bs-panel-footer">
                        <div className="bs-metric">
                            <span className="bs-pill-label">Total</span>
                            <span className="bs-panel-price">{money(totalPrice)}</span>
                        </div>
                        <div className="bs-metric">
                            <span className="bs-pill-label">Weight</span>
                            <span className="bs-panel-weight">{totalWeight > 0 ? `${totalWeight.toFixed(0)} g` : '—'}</span>
                        </div>
                        <button
                            className="bb-btn-primary bs-finish-pill"
                            onClick={() => navigate("/builds/new/review")}
                            disabled={!hasComponents}
                        >
                            Finish build
                        </button>
                    </div>
                </aside>
            </div>
        </div>
    );
};

export default BikeStageBuilder;
