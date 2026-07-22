import { useState, useEffect, useRef } from "react";
import { fetchComponentsByCategory } from "../../services/componentService";
import { useComponentFilters } from "../../hooks/useComponentFilters";
import FilterSidebar from "../../components/Filters/FilterSidebar";
import ImportModal from "./ImportModal";
import CategoryIcon from "../../components/Icons/CategoryIcons";
import "./Components.css";
import ComponentCard, { ComponentCardSkeleton } from "../../components/BikeComponents/ComponentCard";

const Components = () => {
    const filters = useComponentFilters();
    const { query } = filters;
    const [components, setComponents] = useState([]);
    const [total, setTotal] = useState(0);
    const [loading, setLoading] = useState(false);
    const [importOpen, setImportOpen] = useState(false);
    const [reloadToken, setReloadToken] = useState(0);
    const rowRef = useRef(null);

    const scrollRow = (dir) => {
        rowRef.current?.scrollBy({ left: dir * 240, behavior: "smooth" });
    };

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

    return (
        <div className="page components-page">
            <div className="components-header">
                <div>
                    <h1 className="components-title">{total} Products </h1>
                </div>
            </div>

            <div className="component-quick-search-container">
                <button type="button" className="quick-nav" onClick={() => scrollRow(-1)} aria-label="Previous">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M15 6l-6 6 6 6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </button>
                <div className="quick-filter-row" ref={rowRef}>
                    {filters.componentTypes.map((type) => (
                        <button
                            key={type.value}
                            type="button"
                            title={type.label}
                            className={`quick-filter${filters.type === type.value ? " is-active" : ""}`}
                            onClick={() => filters.selectType(filters.type === type.value ? "" : type.value)}
                        >
                            <CategoryIcon category={type.value} />
                        </button>
                    ))}
                </div>
                <button type="button" className="quick-nav" onClick={() => scrollRow(1)} aria-label="Next">
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path d="M9 6l6 6-6 6" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                </button>
            </div>

            <div className="components-toolbar">
                <div className="filter-search">
                    <svg className="filter-search-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
                        <path d="M16.5 16.5L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    <input
                        id="filter-search"
                        type="search"
                        className="filter-search-input"
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

            <div className="components-body">
                <FilterSidebar filters={filters} />

                <div className="components-results">
                {loading ? (
                        <div className="product-grid" aria-hidden="true">
                            {Array.from({ length: 10 }, (_, i) => (
                                <ComponentCardSkeleton key={i} />
                            ))}
                        </div>
                    ) : components.length === 0 ? (
                        <div className="product-empty">
                            <p className="product-empty-title">No components match</p>
                            <p className="product-empty-hint">
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
                                <ComponentCard 
                                    key={comp.id}
                                    comp={comp}/>
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
