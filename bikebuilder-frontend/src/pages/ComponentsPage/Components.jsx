import { useState, useEffect } from "react";
import { fetchComponentsByCategory, fetchBrands, fetchComponentTypes } from "../../services/componentService";
import BrandCombobox from "./BrandCombobox";
import ImportModal from "./ImportModal";
import "./Components.css";

const Components = () => {
    const [type, setType] = useState("");
    const [componentTypes, setComponentTypes] = useState([]);
    const [components, setComponents] = useState([]);
    const [priceMin, setPriceMin] = useState("");
    const [priceMax, setPriceMax] = useState("");
    const [loading, setLoading] = useState(false);
    const [brands, setBrands] = useState([]);
    const [brand, setBrand] = useState("");
    const [search, setSearch] = useState("");
    const [filtersOpen, setFiltersOpen] = useState(false);
    const [importOpen, setImportOpen] = useState(false);
    const [reloadToken, setReloadToken] = useState(0);

    const selectType = (nextType) => {
        setType(nextType);
        setBrand("");
    };

    useEffect(() => {
        fetchComponentTypes()
            .then(data => setComponentTypes(data))
            .catch(err => console.log(err));
    }, []);

    useEffect(() => {
        fetchBrands(type)
            .then(data => setBrands(data))
            .catch(err => console.log(err));
    }, [type]);

    useEffect(() => {
        const timer = setTimeout(() => {
            setLoading(true);
            fetchComponentsByCategory(type, search, brand, priceMin, priceMax)
                .then(data => setComponents(data))
                .catch(err => console.log(err))
                .finally(() => setLoading(false));
        }, 300);
        return () => clearTimeout(timer);
    }, [type, search, brand, priceMin, priceMax, reloadToken]);

    const typeLabels = Object.fromEntries(componentTypes.map(t => [t.value, t.label]));

    const clearFilters = () => {
        setType("");
        setBrand("");
        setSearch("");
        setPriceMin("");
        setPriceMax("");
    };

    const hasFilters = type || brand || search || priceMin || priceMax;
    const activeCount = [type, brand, priceMin || priceMax].filter(Boolean).length;

    return (
        <div className="components-page">
            <div className="components-header">
                <div>
                    <h2 className="components-title">Products</h2>
                    <p className="components-subtitle">{components.length} products</p>
                </div>
            </div>

            <div className="components-toolbar">
                <div className="toolbar-search">
                    <svg className="toolbar-search-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
                        <path d="M16.5 16.5L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    <input
                        id="filter-search"
                        type="search"
                        className="toolbar-search-input"
                        placeholder="Search products..."
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                    />
                </div>

                <button
                    type="button"
                    className="filter-toggle"
                    onClick={() => setImportOpen(true)}
                >
                    Import
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path
                            d="M12 5v14M5 12h14"
                            stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                        />
                    </svg>
                </button>

                <button
                    type="button"
                    className={`filter-toggle${filtersOpen ? " is-open" : ""}`}
                    aria-expanded={filtersOpen}
                    onClick={() => setFiltersOpen(o => !o)}
                >
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path
                            d="M4 6h16M7 12h10M10 18h4"
                            stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                        />
                    </svg>
                    Filter
                    {activeCount > 0 && <span className="filter-badge">{activeCount}</span>}
                </button>
            </div>

            {filtersOpen && (
                <div className="filter-panel" role="region" aria-label="Filters">
                    <div className="filter-group">
                        <label className="filter-label" htmlFor="filter-type">Type</label>
                        <select
                            id="filter-type"
                            className="filter-select"
                            value={type}
                            onChange={e => selectType(e.target.value)}
                        >
                            <option value="">All types</option>
                            {componentTypes.map(t => (
                                <option key={t.value} value={t.value}>{t.label}</option>
                            ))}
                        </select>
                    </div>

                    <div className="filter-group">
                        <label className="filter-label" htmlFor="filter-brand">Brand</label>
                        <BrandCombobox brands={brands} value={brand} onChange={setBrand} />
                    </div>

                    <div className="filter-group">
                        <label className="filter-label" htmlFor="filter-price-min">Price</label>
                        <div className="filter-price-row">
                            <input
                                id="filter-price-min"
                                type="number"
                                min="0"
                                className="filter-input"
                                placeholder="Min"
                                value={priceMin}
                                onChange={e => setPriceMin(e.target.value)}
                            />
                            <span className="filter-price-sep">–</span>
                            <input
                                id="filter-price-max"
                                type="number"
                                min="0"
                                className="filter-input"
                                placeholder="Max"
                                value={priceMax}
                                onChange={e => setPriceMax(e.target.value)}
                            />
                        </div>
                    </div>

                    {hasFilters && (
                        <button
                            type="button"
                            className="filter-clear"
                            onClick={clearFilters}
                        >
                            Clear filters
                        </button>
                    )}
                </div>
            )}

            <div className="components-results">
                {loading ? (
                        <div className="product-grid" aria-hidden="true">
                            {Array.from({ length: 6 }, (_, i) => (
                                <div key={i} className="product-card is-skeleton">
                                    <div className="product-media" />
                                    <div className="product-card-body">
                                        <span className="skeleton-line skeleton-line--brand" />
                                        <span className="skeleton-line skeleton-line--name" />
                                    </div>
                                    <div className="product-card-footer">
                                        <span className="skeleton-line skeleton-line--price" />
                                    </div>
                                </div>
                            ))}
                        </div>
                    ) : components.length === 0 ? (
                        <div className="products-empty">
                            <p className="products-empty-title">No components match</p>
                            <p className="products-empty-hint">
                                Try widening the price range or clearing a filter.
                            </p>
                            {hasFilters && (
                                <button type="button" className="filter-clear" onClick={clearFilters}>
                                    Clear filters
                                </button>
                            )}
                        </div>
                    ) : (
                        <div className="product-grid">
                            {components.map(comp => (
                                <article key={comp.id} className="product-card">
                                    <div className="product-media">
                                        {comp.image_url ? (
                                            <img src={comp.image_url} alt={comp.name} loading="lazy" />
                                        ) : (
                                            <svg className="product-media-placeholder" viewBox="0 0 48 48" aria-hidden="true">
                                                <circle cx="24" cy="24" r="15" fill="none" stroke="currentColor" strokeWidth="2" />
                                                <circle cx="24" cy="24" r="5.5" fill="none" stroke="currentColor" strokeWidth="2" />
                                                <path
                                                    d="M24 9v6.5M24 32.5V39M9 24h6.5M32.5 24H39M13.4 13.4l4.6 4.6M30 30l4.6 4.6M34.6 13.4L30 18M18 30l-4.6 4.6"
                                                    stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                                                />
                                            </svg>
                                        )}
                                        <span className="product-type">
                                            {typeLabels[comp.component_type] || comp.component_type}
                                        </span>
                                    </div>
                                    <div className="product-card-body">
                                        <p className="product-brand">{comp.brand}</p>
                                        <h3 className="product-name">{comp.name}</h3>
                                        {comp.description && (
                                            <p className="product-desc">{comp.description}</p>
                                        )}
                                    </div>
                                    <div className="product-card-footer">
                                        <span className="product-price">${comp.price}</span>
                                        <span className="product-weight">{comp.weight_grams}g</span>
                                    </div>
                                </article>
                            ))}
                        </div>
                    )}
                </div>

                {importOpen && (
                    <ImportModal
                        onClose={() => setImportOpen(false)}
                        onImported={() => setReloadToken(t => t + 1)}
                    />
                )}
            </div>
    );
};

export default Components;
