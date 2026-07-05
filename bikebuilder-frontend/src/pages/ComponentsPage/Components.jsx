import { useState, useEffect } from "react";
import { fetchComponentsByCategory } from "../../services/componentService";
import { useComponentFilters } from "../../hooks/useComponentFilters";
import FilterSidebar from "../../components/Filters/FilterSidebar";
import ImportModal from "./ImportModal";
import "./Components.css";

const Components = () => {
    const filters = useComponentFilters();
    const { query } = filters;

    const [components, setComponents] = useState([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(false);
    const [importOpen, setImportOpen] = useState(false);
    const [reloadToken, setReloadToken] = useState(0);

    useEffect(() => {
        setLoading(true);
        fetchComponentsByCategory(query.type, query.search, query.brand, query.priceMin, query.priceMax)
            .then(data => {
                setComponents(data.results);
                setTotal(data.count);
            })
            .catch(err => console.log(err))
            .finally(() => setLoading(false));
    }, [query.type, query.search, query.brand, query.priceMin, query.priceMax, reloadToken]);

    const typeLabels = Object.fromEntries(filters.componentTypes.map(t => [t.value, t.label]));

    return (
        <div className="components-page">
            <div className="components-header">
                <div>
                    <h1 className="components-title">{total} Products </h1>
                </div>
            </div>

            <div className="cmp-toolbar-row">
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
                        value={filters.search}
                        onChange={e => filters.setSearch(e.target.value)}
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
            </div>

            <div className="cmp-body">
                <FilterSidebar filters={filters} />

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
                            {filters.hasFilters && (
                                <button type="button" className="filter-clear" onClick={filters.clearFilters}>
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
