import BrandSelectBox from "./BrandSelectBox";

// Just the filter inputs. Row-vs-column layout is decided by the parent's CSS,
// not here, so this drops cleanly into both the toolbar panel and the sidebar.
const FilterFields = ({ filters }) => {
    const {
        type, brand, priceMin, priceMax, weightMax, weightMin,
        setBrand, setPriceMin, setPriceMax, setWeightMax, setWeightMin, selectType,
        componentTypes, brands, typeLocked,
        hasFilters, clearFilters,
    } = filters;

    return (
        <>
            {!typeLocked && (
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
            )}

            <div className="filter-group">
                <label className="filter-label" htmlFor="filter-brand">Brand</label>
                <BrandSelectBox brands={brands} value={brand} onChange={setBrand} />
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
                <label className="filter-label" htmlFor="filter-weight-min">Weight</label>
                <div className="filter-price-row">
                    <input
                        id="filter-weight-min"
                        type="number"
                        min="0"
                        className="filter-input"
                        placeholder="Min"
                        value={weightMin}
                        onChange={e => setWeightMin(e.target.value)}
                    />
                    <span className="filter-price-sep">–</span>
                    <input
                        id="filter-weight-max"
                        type="number"
                        min="0"
                        className="filter-input"
                        placeholder="Max"
                        value={weightMax}
                        onChange={e => setWeightMax(e.target.value)}
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
        </>
    );
};

export default FilterFields;
