import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import BikeCanvas from "../../../bike3d/BikeCanvas";
import "../../../styles/pages/Builds/Builds.css";
import ProgressSteps from "./ProgressSteps";
import FilterBar from "../../../components/Filters/FilterBar";
import ComponentCard, { ComponentCardSkeleton } from "../../../components/BikeComponents/ComponentCard";
import { useComponentFilters } from "../../../hooks/useComponentFilters";
import { titleCase, money, sumPrice, sumWeight } from "../../../utils/format";
import { fetchComponentsByCategory, fetchCompatibleComponents, createCustomWheel } from "../../../services/componentService";

const ASSEMBLY_ORDER = [
    "frame", "bottom_bracket", "crank", "crankset", "wheels", "front_wheel", "rear_wheel", "wheelset",
    "chainring", "sprocket", "chain", "tire", "seatpost", "saddle", "stem", "brake",
    "handlebar", "pedals",
];

const modeSummary = modeCfg =>
    (modeCfg.required || []).map(titleCase).join(' + ');

const GroupModes = ({ group, mode, locked, prereq, onChooseMode }) => {
    if (locked) return <p className="bs-group-locked">Select {titleCase(prereq).toLowerCase()} first</p>;
    return (
        <div className="bs-mode-cards">
            {Object.entries(group.modes).map(([key, cfg]) => (
                <button
                    key={key}
                    type="button"
                    className={`bs-mode-card${mode === key ? ' is-active' : ''}`}
                    onClick={() => onChooseMode(key)}
                >
                    <span className="bs-mode-card-title">{cfg.label ?? titleCase(key)}</span>
                    <span className="bs-mode-card-sub">{modeSummary(cfg)}</span>
                </button>
            ))}
        </div>
    );
};

const BikeStageBuilder = () => {
    const { build, emptyBuild, addComponent } = useBuild();
    const navigate = useNavigate();
    const [focusedCategory, setFocusedCategory] = useState(null);
    const { required = [], optional = [], prerequisites = {}, groups = {} } = build.bikeType.rules;

    const [groupModes, setGroupModes] = useState(() =>
        Object.fromEntries(Object.entries(groups).map(([key, g]) => [key, g.default]))
    );

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const allCategories = [...required, ...optional];

    const orderedCats = [
        ...ASSEMBLY_ORDER.filter(c => allCategories.includes(c)),
        ...allCategories.filter(c => !ASSEMBLY_ORDER.includes(c)),
    ];

    const activeCategory = focusedCategory ?? orderedCats[0];
    const activeGroup = groups[activeCategory] ?? null;
    const activeMode = activeGroup ? activeGroup.modes[groupModes[activeCategory]] : null;

    const modeParts = activeMode
        ? [...(activeMode.required || []), ...(activeMode.optional || [])]
        : [];

    const partLocked = part => {
        const dep = (activeMode.prerequisites || {})[part];
        return !!dep && !selectedByCategory[dep];
    };

    const [groupPart, setGroupPart] = useState(null);
    const partUsable = part => modeParts.includes(part) && !partLocked(part);
    const activePart = partUsable(groupPart)
        ? groupPart
        : modeParts.find(p => !partLocked(p) && !selectedByCategory[p])
            ?? modeParts.find(p => !partLocked(p));

    const [customHub, setCustomHub] = useState(null);
    const isCustom = activeMode?.builder === "custom";
    const wheelPosition = activePart === "front_wheel" ? "front" : "rear";
    const customType = customHub ? "rim" : "track_hub";

    const selectingCategory = !activeGroup
        ? activeCategory
        : isCustom && activePart ? customType : activePart;

    const selectedId = isCustom
        ? customHub && selectingCategory === "track_hub" ? customHub.id : null
        : selectedByCategory[selectingCategory]?.id;

    const endLabel = wheelPosition === "front" ? "Front" : "Rear";

    const selectTitle = isCustom
        ? `${endLabel} ${customType === "rim" ? "rim" : "hub"}`
        : titleCase(selectingCategory);

    const choosePart = part => {
        setGroupPart(part);
        setCustomHub(null);
    };

    const nextPart = () => modeParts[modeParts.indexOf(activePart) + 1] ?? null;

    const handleSelect = async comp => {
        if (!isCustom) {
            addComponent(comp);
            if (activeGroup) setGroupPart(nextPart());
            return;
        }
        if (!customHub) {
            setCustomHub(comp);
            return;
        }
        try {
            const wheel = await createCustomWheel({ position: wheelPosition, hubId: customHub.id, rimId: comp.id });
            addComponent(wheel);
            choosePart(nextPart());
        } catch (e) {
            console.error(e);
        }
    };

    const filters = useComponentFilters({ fixedType: selectingCategory || "" });
    const { query } = filters;
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(false);

    const getSelectedIds = () => ({
        ...Object.fromEntries(
            Object.values(selectedByCategory).map(c => [`${c.component_type}_id`, c.id])
        ),
        ...(isCustom && { position: wheelPosition, custom_hub_id: customHub?.id }),
    });

    const modeOf = category => groups[category].modes[groupModes[category]];

    const isFilled = category => {
        if (!groups[category]) return !!selectedByCategory[category];
        return (modeOf(category).required || []).every(t => selectedByCategory[t]);
    };

    const isLocked = category => {
        const dep = prerequisites[category];
        return dep && allCategories.includes(dep) && !isFilled(dep);
    };

    const categoryLabel = category =>
        groups[category] ? groups[category].label : titleCase(category);

    const steps = orderedCats.map(category => ({
        key: category,
        label: categoryLabel(category),
        filled: isFilled(category),
        locked: isLocked(category),
    }));

    const nextCategory = orderedCats
        .slice(orderedCats.indexOf(activeCategory) + 1)
        .find(c => !isLocked(c));

    const totalPrice = sumPrice(build.components);
    const totalWeight = sumWeight(build.components);

    const hasComponents = build.components.length > 0;

    const compatCount = components.filter(c => c.compatible).length;

    const handleStartOver = () => {
        emptyBuild();
        navigate("/builds/new");
    };

    useEffect(() => {
        if (!selectingCategory) return;
        const load = async () => {
            setLoading(true);
            setComponents([]);
            try {
                const [all, compatible] = await Promise.all([
                    fetchComponentsByCategory(selectingCategory, query.search, query.brand, query.priceMin, query.priceMax),
                    selectingCategory === "frame"
                        ? Promise.resolve(null)
                        : fetchCompatibleComponents(selectingCategory, getSelectedIds()),
                ]);
                const allResults = all.results;
                const compatibleIds = new Set((compatible ?? allResults).map(c => c.id));
                setComponents(allResults.map(c => ({ ...c, compatible: compatibleIds.has(c.id) })));
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [selectingCategory, activePart, query.search, query.brand, query.priceMin, query.priceMax]);

    return (
        <div className="bb-wrapper bs-wrapper">
            <div className="bs-stage-layout">
                <div className="bs-stage-left">
                    <ProgressSteps
                        steps={steps}
                        focused={activeCategory}
                        onFocus={setFocusedCategory}
                    />
                    <div className="bs-canvas">
                        <BikeCanvas />
                        {!hasComponents && (
                            <div className="bs-canvas-hint">
                            <span className="bs-canvas-title">
                                {"3D preview \n Select a part to focus the view"}
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
                        <button className="bb-btn-ghost bs-startover-pill" onClick={handleStartOver}>
                            Start Over
                        </button>
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
                        <div className="bs-panel-filters">
                            <FilterBar filters={filters} iconOnly />
                        </div>
                        {activeGroup && (
                            <>
                                <GroupModes
                                    group={activeGroup}
                                    mode={groupModes[activeCategory]}
                                    locked={isLocked(activeCategory)}
                                    prereq={prerequisites[activeCategory]}
                                    onChooseMode={mode => {
                                        setGroupModes(prev => ({ ...prev, [activeCategory]: mode }));
                                        choosePart(null);
                                    }}
                                />
                                {modeParts.length > 1 && (
                                    <div className="bs-part-tabs">
                                        {modeParts.map(part => {
                                            const locked = partLocked(part);
                                            const sel = selectedByCategory[part];
                                            return (
                                                <button
                                                    key={part}
                                                    type="button"
                                                    className={`bs-part-tab${part === activePart ? ' is-active' : ''}${sel ? ' is-filled' : ''}`}
                                                    disabled={locked}
                                                    onClick={() => choosePart(part)}
                                                >
                                                    <span className="bs-part-tab-name">{titleCase(part)}</span>
                                                    <span className="bs-part-tab-val">
                                                        {sel ? sel.name : locked ? `Select ${titleCase(activeMode.prerequisites[part])} first` : 'Not selected'}
                                                    </span>
                                                </button>
                                            );
                                        })}
                                    </div>
                                )}
                                {isCustom && activePart && (
                                    <div className="bs-part-tabs">
                                        <button
                                            type="button"
                                            className={`bs-part-tab${customType === "track_hub" ? ' is-active' : ' is-filled'}`}
                                            onClick={() => setCustomHub(null)}
                                        >
                                            <span className="bs-part-tab-name">{endLabel} hub</span>
                                            <span className="bs-part-tab-val">{customHub ? customHub.name : 'Not selected'}</span>
                                        </button>
                                        <button
                                            type="button"
                                            className={`bs-part-tab${customType === "rim" ? ' is-active' : ''}`}
                                            disabled={!customHub}
                                        >
                                            <span className="bs-part-tab-name">{endLabel} rim</span>
                                            <span className="bs-part-tab-val">{customHub ? 'Not selected' : 'Select a hub first'}</span>
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                        {!selectingCategory ? null : (
                            <>
                                <div className="bs-select-head">
                                    <div className="bs-select-title">
                                        {selectTitle}
                                        {!loading && (
                                            <span className="bs-select-count">
                                                {compatCount} compatible
                                                {components.length > compatCount && ` · ${components.length - compatCount} incompatible`}
                                            </span>
                                        )}
                                    </div>
                                </div>
                                {loading ? (
                                    <div className="bs-product-grid">
                                        {Array.from({ length: 4 }).map((_, i) => <ComponentCardSkeleton key={i} />)}
                                    </div>
                                ) : components.length === 0 ? (
                                    <p className="empty-state">No {titleCase(selectingCategory).toLowerCase()} components found.</p>
                                ) : (
                                    <div className="bs-product-grid">
                                        {components.map(comp => (
                                            <ComponentCard
                                                key={comp.id}
                                                comp={comp}
                                                isSelected={comp.id === selectedId}
                                                onSelect={handleSelect}
                                            />
                                        ))}
                                    </div>
                                )}
                            </>
                        )}
                    </div>

                    {nextCategory && (
                        <div className="bs-panel-next-bar">
                            <button
                                type="button"
                                className="bb-btn-primary bs-panel-next"
                                onClick={() => setFocusedCategory(nextCategory)}
                            >
                                Continue to {categoryLabel(nextCategory)}
                            </button>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default BikeStageBuilder;
