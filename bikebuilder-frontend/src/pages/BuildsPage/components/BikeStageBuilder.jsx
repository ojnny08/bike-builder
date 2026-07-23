import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import BikeCanvas from "../../../threejs/3d-bike/BikeCanvas";
import CategoryIcon from "../../../components/Icons/CategoryIcons";
import "../style/Builds.css";
import BuilderNav from "./BuilderNav";

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

const PartCard = ({ category, selected, focused, locked, prereq, onFocus, onChoose }) => (
    <div
        className={`bs-card${selected ? ' is-filled' : ''}${focused ? ' is-focused' : ''}${locked ? ' is-locked' : ''}`}
        role="button"
        tabIndex={locked ? -1 : 0}
        aria-pressed={focused}
        aria-disabled={locked}
        onClick={locked ? undefined : onFocus}
        onDoubleClick={locked ? undefined : onChoose}
    >
        
        <div className="bs-card-main">
            <span className="bs-card-placeholder">{formatCat(category)}</span>
            
            {selected ? (
                <span className="bs-card-name">
                    {selected.name}
                    <span className="bs-card-meta"> · {money(parseFloat(selected.price) || 0)}</span>
                </span>
            ) : locked ? (
                <span className="bs-card-cat">Select {formatCat(prereq)} first</span>
            ) : (
                <span className="bs-card-cat">Not Selected</span>
            )}
        </div>
        <span className="bs-card-icon"><CategoryIcon category={category} /></span>
        {!locked && focused ? (
            <button
                type="button"
                className="bs-card-add"
                aria-label={`Choose ${formatCat(category).toLowerCase()}`}
                onClick={e => { e.stopPropagation(); onChoose(); }}
            >
                <PlusGlyph />
            </button>
        ) : (
            ""
        )}
        {}
    </div>
);

const BikeStageBuilder = () => {
    const { build, emptyBuild } = useBuild();
    const navigate = useNavigate();
    const [focusedCategory, setFocusedCategory] = useState(null);
    const [componentList, setComponentList] = useState(false);
    const { required = [], optional = [], prerequisites = {} } = build.bikeType.rules;

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const allCategories = [...required, ...optional];

    const isLocked = category => {
        const dep = prerequisites[category];
        return dep && allCategories.includes(dep) && !selectedByCategory[dep];
    };
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
            <BuilderNav />
            <div className="bs-stage-layout">
                <div className="bs-stage-left">
                    <div className="bs-canvas">
                        <BikeCanvas />
                        {!hasComponents && (
                            <div className="bs-canvas-hint">
                            <span className="bs-canvas-title">
                                {componentList ? "" : "3D preview \n Select a part to focus the view"}
                            </span>
                        </div>
                        )}
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
                            Finish Build
                        </button>
                    </div>
                </div>

                <div className="bs-panel">
                    <div className="bs-panel-list">
                        {orderedCats.map(category => (
                            <PartCard
                                key={category}
                                category={category}
                                selected={selectedByCategory[category]}
                                focused={focusedCategory === category}
                                locked={isLocked(category)}
                                prereq={prerequisites[category]}
                                onFocus={() => setFocusedCategory(category)}
                                onChoose={() => navigate(`/builds/new/select/${category}`)}
                            />
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BikeStageBuilder;
