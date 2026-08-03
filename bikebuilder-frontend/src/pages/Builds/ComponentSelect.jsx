import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useBuild } from "../../context/BuildContext";
import { fetchComponentsByCategory, fetchCompatibleComponents } from "../../services/componentService";
import { useComponentFilters } from "../../hooks/useComponentFilters";
import FilterBar from "../../components/Filters/FilterBar";
import BuilderNav from "./components/BuilderNav";
import ComponentCard, { ComponentCardSkeleton } from "../../components/BikeComponents/ComponentCard";
import { titleCase } from "../../utils/format";
import "./style/Builds.css";

const PartGlyph = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4"
        strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="3.2" />
        <path d="M12 2.6v3M12 18.4v3M2.6 12h3M18.4 12h3M5.4 5.4l2.1 2.1M16.5 16.5l2.1 2.1M18.6 5.4l-2.1 2.1M7.5 16.5l-2.1 2.1" />
    </svg>
);



const ComponentSelect = () => {
    const { category: paramCategory, group, mode } = useParams();
    const { build } = useBuild();
    const navigate = useNavigate();

    const isGroup = !!group;
    const activeMode = isGroup ? build.bikeType.rules.groups[group].modes[mode] : null;
    const groupPrereqs = isGroup ? (activeMode.prerequisites || {}) : {};
    const groupParts = isGroup ? [...(activeMode.required || []), ...(activeMode.optional || [])] : [];

    const isMultiPart = isGroup && (activeMode.required || []).length > 1;

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const [currentPart, setCurrentPart] = useState(() => groupParts[0]);
    const category = isGroup ? currentPart : paramCategory;

    const chosen = selectedByCategory;

    const filters = useComponentFilters({ fixedType: category });
    const { query } = filters;
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(true);

    const openDetail = comp => navigate(
        isGroup
            ? `/builds/new/select-group/${group}/${mode}/${comp.id}`
            : `/builds/new/select/${category}/${comp.id}`
    );

    const currentSelectedId = chosen[category]?.id;
    const partLocked = part => {
        const dep = groupPrereqs[part];
        return dep && !chosen[dep];
    };
    const requiredComplete = isGroup && (activeMode.required || []).every(t => chosen[t]);

    const getSelectedIds = () =>
        Object.fromEntries(Object.values(chosen).map(c => [`${c.component_type}_id`, c.id]));

    useEffect(() => {
        const load = async () => {
            setLoading(true);
            try {
                const selectedIds = getSelectedIds();
                const [all, compatible] = await Promise.all([
                    fetchComponentsByCategory(category, query.search, query.brand, query.priceMin, query.priceMax),
                    category === 'frame'
                        ? Promise.resolve(null)
                        : fetchCompatibleComponents(category, selectedIds),
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
    }, [category, query.search, query.brand, query.priceMin, query.priceMax]);

    const compatCount = components.filter(c => c.compatible).length;

    return (
        <div className="bb-wrapper">
        <BuilderNav onSave={() => navigate("/builds/new/review")} />
        <div className={isGroup ? "cs-page cs-group-layout" : "cs-page"}>
            {isGroup && (
                <aside className="cs-side">
                    <h2 className="cs-side-title">{build.bikeType.rules.groups[group].label}</h2>
                    <ul className="cs-side-list">
                        {groupParts.map(part => {
                            const sel = chosen[part];
                            const locked = partLocked(part);
                            const optional = !(activeMode.required || []).includes(part);
                            return (
                                <li key={part}>
                                    <button
                                        type="button"
                                        className={`cs-side-part${part === category ? ' is-active' : ''}${locked ? ' is-locked' : ''}`}
                                        disabled={locked}
                                        onClick={() => setCurrentPart(part)}
                                    >
                                        <span className="cs-side-part-name">
                                            {titleCase(part)}{optional ? ' (optional)' : ''}
                                        </span>
                                        <span className="cs-side-part-val">
                                            {sel ? sel.name : locked ? `Select ${titleCase(groupPrereqs[part])} first` : 'Not selected'}
                                        </span>
                                    </button>
                                </li>
                            );
                        })}
                    </ul>
                    <button
                        type="button"
                        className="bb-btn-primary cs-side-done"
                        disabled={!requiredComplete}
                        onClick={() => navigate("/builds/new")}
                    >
                        {isMultiPart ? "Save to build" : "Back to builder"}
                    </button>
                </aside>
            )}
            <div className="cs-group-main">
            <header className="cs-head">
                <div className="cs-head-text">
                    <h1 className="cs-head-title"> Select A {titleCase(category)}</h1>
                    {!loading && (
                        <p className="cs-head-sub">
                            {compatCount} compatible
                            {components.length > compatCount && ` · ${components.length - compatCount} incompatible`}
                        </p>
                    )}
                </div>
            </header>

            <FilterBar filters={filters} iconOnly centered />

            {loading ? (
                <div className="product-grid">
                    {Array.from({ length: 10 }).map((_, i) => <ComponentCardSkeleton key={i} />)}
                </div>
            ) : components.length === 0 ? (
                <p className="empty-state">No {titleCase(category).toLowerCase()} components found.</p>
            ) : (
                <div className="cs-grid">
                    {components.map(comp => (
                        <ComponentCard
                            key={comp.id}
                            comp={comp}
                            isSelected={comp.id === currentSelectedId}
                            onSelect={openDetail}
                        />
                    ))}
                </div>
            )}
            </div>
        </div>
        </div>
    );
};

export default ComponentSelect;
