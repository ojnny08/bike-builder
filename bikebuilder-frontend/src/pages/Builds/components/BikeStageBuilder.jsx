import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import BikeCanvas from "../../../threejs/3d-bike/BikeCanvas";
import CategoryIcon from "../../../components/Icons/CategoryIcons";
import "../style/Builds.css";
import BuilderNav from "./BuilderNav";
import { titleCase, money, sumPrice, sumWeight } from "../../../utils/format";

const ASSEMBLY_ORDER = [
    "frame", "bottom_bracket", "crank", "crankset", "wheels", "wheel", "wheelset",
    "chainring", "sprocket", "chain", "tire", "seatpost", "saddle", "stem", "brake",
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
            <span className="bs-card-placeholder">{titleCase(category)}</span>
            
            {selected ? (
                <span className="bs-card-name">
                    {selected.name}
                    <span className="bs-card-meta"> · {money(selected.price)}</span>
                </span>
            ) : locked ? (
                <span className="bs-card-cat">Select {titleCase(prereq)} first</span>
            ) : (
                <span className="bs-card-cat">Not Selected</span>
            )}
        </div>
        <span className="bs-card-icon"><CategoryIcon category={category} /></span>
        {!locked && focused ? (
            <button
                type="button"
                className="bs-card-add"
                aria-label={`Choose ${titleCase(category).toLowerCase()}`}
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

const modeSummary = modeCfg =>
    (modeCfg.required || []).map(titleCase).join(' + ');

const GroupCard = ({ group, groupKey, mode, parts, filled, focused, locked, prereq, onFocus, onChooseMode }) => {
    const total = sumPrice(parts);
    return (
        <div
            className={`bs-card${filled ? ' is-filled' : ''}${focused ? ' is-focused' : ''}${locked ? ' is-locked' : ''}`}
            role="button"
            tabIndex={locked ? -1 : 0}
            aria-pressed={focused}
            aria-disabled={locked}
            onClick={locked ? undefined : onFocus}
        >
            {focused && !locked && (
                <div className="bs-mode-cards">
                    {Object.entries(group.modes).map(([key, cfg]) => (
                        <button
                            key={key}
                            type="button"
                            className={`bs-mode-card${mode === key ? ' is-active' : ''}`}
                            onClick={e => { e.stopPropagation(); onChooseMode(key); }}
                        >
                            <span className="bs-mode-card-title">{titleCase(key)}</span>
                            <span className="bs-mode-card-sub">{modeSummary(cfg)}</span>
                        </button>
                    ))}
                </div>
            )}
            <div className="bs-card-main">
                <span className="bs-card-placeholder">{group.label}</span>

                {filled ? (
                    <span className="bs-card-name">
                        {parts.map(p => p.name).join(' + ')}
                        <span className="bs-card-meta"> · {money(total)}</span>
                    </span>
                ) : locked ? (
                    <span className="bs-card-cat">Select {titleCase(prereq)} first</span>
                ) : (
                    <span className="bs-card-cat">Not Selected</span>
                )}
            </div>
            <span className="bs-card-icon"><CategoryIcon category={groupKey} /></span>
        </div>
    );
};

const BikeStageBuilder = () => {
    const { build, emptyBuild } = useBuild();
    const navigate = useNavigate();
    const [focusedCategory, setFocusedCategory] = useState(null);
    const [componentList, setComponentList] = useState(false);
    const { required = [], optional = [], prerequisites = {}, groups = {} } = build.bikeType.rules;

    const [groupModes, setGroupModes] = useState(() =>
        Object.fromEntries(Object.entries(groups).map(([key, g]) => [key, g.default]))
    );

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const allCategories = [...required, ...optional];

    const modeConfig = (category, mode) => groups[category].modes[mode];
    const activeMode = category => modeConfig(category, groupModes[category]);

    const groupParts = category => {
        const mode = activeMode(category);
        return [...(mode.required || []), ...(mode.optional || [])]
            .map(t => selectedByCategory[t])
            .filter(Boolean);
    };

    const isFilled = category => {
        if (!groups[category]) return !!selectedByCategory[category];
        return (activeMode(category).required || []).every(t => selectedByCategory[t]);
    };

    const groupRoute = (category, mode) => {
        const { required: req = [], optional: opt = [] } = modeConfig(category, mode);
        if (req.length === 1 && opt.length === 0) return `/builds/new/select/${req[0]}`;
        return `/builds/new/select-group/${category}/${mode}`;
    };

    const isLocked = category => {
        const dep = prerequisites[category];
        return dep && allCategories.includes(dep) && !isFilled(dep);
    };
    const orderedCats = [
        ...ASSEMBLY_ORDER.filter(c => allCategories.includes(c)),
        ...allCategories.filter(c => !ASSEMBLY_ORDER.includes(c)),
    ];

    const requiredFilled = required.filter(isFilled).length;
    const progress = required.length ? requiredFilled / required.length : 0;

    const totalPrice = sumPrice(build.components);
    const totalWeight = sumWeight(build.components);

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
                            groups[category] ? (
                                <GroupCard
                                    key={category}
                                    group={groups[category]}
                                    groupKey={category}
                                    mode={groupModes[category]}
                                    parts={groupParts(category)}
                                    filled={isFilled(category)}
                                    focused={focusedCategory === category}
                                    locked={isLocked(category)}
                                    prereq={prerequisites[category]}
                                    onFocus={() => setFocusedCategory(category)}
                                    onChooseMode={mode => {
                                        setGroupModes(prev => ({ ...prev, [category]: mode }));
                                        navigate(groupRoute(category, mode));
                                    }}
                                />
                            ) : (
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
                            )
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BikeStageBuilder;
