import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useBuild } from "../../context/BuildContext";
import { fetchComponentsByCategory, fetchCompatibleComponents } from "../../services/componentService";
import "./style/Builds.css";

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

const PartGlyph = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4"
        strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="3.2" />
        <path d="M12 2.6v3M12 18.4v3M2.6 12h3M18.4 12h3M5.4 5.4l2.1 2.1M16.5 16.5l2.1 2.1M18.6 5.4l-2.1 2.1M7.5 16.5l-2.1 2.1" />
    </svg>
);

const ComponentCard = ({ comp, isSelected, onSelect }) => {
    const blocked = !comp.compatible;
    return (
        <button
            type="button"
            className={`cs-card${blocked ? ' is-blocked' : ''}${isSelected ? ' is-selected' : ''}`}
            onClick={() => !blocked && onSelect(comp)}
            disabled={blocked}
            aria-label={`${comp.brand} ${comp.name}, $${comp.price}${blocked ? ', incompatible' : ''}`}
        >
            <div className="cs-card-media">
                {comp.image_url
                    ? <img src={comp.image_url} alt="" loading="lazy" className="cs-card-img" />
                    : <span className="cs-card-glyph"><PartGlyph /></span>}
                {isSelected && (
                    <span className="cs-card-badge cs-card-badge-selected">
                        <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                            <polyline points="20 6 9 17 4 12" />
                        </svg>
                        Selected
                    </span>
                )}
                {blocked && <span className="cs-card-badge cs-card-badge-blocked">Incompatible</span>}
            </div>
            <div className="cs-card-body">
                <span className="cs-card-brand">{comp.brand}</span>
                <span className="cs-card-name">{comp.name}</span>
            </div>
            <div className="cs-card-foot">
                <span className="cs-card-price">
                    {comp.price ? `$${parseFloat(comp.price).toFixed(2)}` : '—'}
                </span>
                {comp.weight_grams ? <span className="cs-card-weight">{comp.weight_grams} g</span> : null}
            </div>
        </button>
    );
};

const ComponentSelectPage = () => {
    const { category } = useParams();
    const { build, addComponent } = useBuild();
    const navigate = useNavigate();
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(true);

    const { prerequisites = {} } = build.bikeType?.rules ?? {};

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );
    const currentSelectedId = selectedByCategory[category]?.id;

    const getSelectedIds = () => {
        const ids = {};
        let current = category;
        while (prerequisites[current]) {
            const dep = prerequisites[current];
            if (selectedByCategory[dep]) ids[`${dep}_id`] = selectedByCategory[dep].id;
            current = dep;
        }
        return ids;
    };

    useEffect(() => {
        const load = async () => {
            try {
                const selectedIds = getSelectedIds();
                const [all, compatible] = await Promise.all([
                    fetchComponentsByCategory(category),
                    category === 'frame'
                        ? Promise.resolve(null)
                        : fetchCompatibleComponents(category, selectedIds),
                ]);
                const compatibleIds = new Set((compatible ?? all).map(c => c.id));
                setComponents(all.map(c => ({ ...c, compatible: compatibleIds.has(c.id) })));
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [category]);

    const handleSelect = (comp) => {
        addComponent(comp);
        navigate("/builds/new");
    };

    const compatCount = components.filter(c => c.compatible).length;

    return (
        <div className="cs-page">
            <header className="cs-head">
                <button className="bb-btn-ghost" onClick={() => navigate("/builds/new")}>← Back to build</button>
                <div className="cs-head-text">
                    <h1 className="cs-head-title">Choose a {formatCat(category)}</h1>
                    {!loading && (
                        <p className="cs-head-sub">
                            {compatCount} compatible
                            {components.length > compatCount && ` · ${components.length - compatCount} incompatible`}
                        </p>
                    )}
                </div>
            </header>

            {loading ? (
                <div className="cs-grid">
                    {Array.from({ length: 8 }).map((_, i) => <div key={i} className="cs-card-skeleton" />)}
                </div>
            ) : components.length === 0 ? (
                <p className="empty-state">No {formatCat(category).toLowerCase()} components found.</p>
            ) : (
                <div className="cs-grid">
                    {components.map(comp => (
                        <ComponentCard
                            key={comp.id}
                            comp={comp}
                            isSelected={comp.id === currentSelectedId}
                            onSelect={handleSelect}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default ComponentSelectPage;
