import FilterFields from "./FilterFields";
import "./FilterSidebar.css";

// Always-open vertical filter rail for the components listing page.
// Shares the actual inputs with FilterBar via FilterFields; only the
// surrounding chrome (compact column, sticky) differs.
const FilterSidebar = ({ filters }) => (
    <aside className="filter-sidebar" aria-label="Filters">
        <div className="filter-sidebar-head">
            <span className="filter-sidebar-title">Filters</span>
            {filters.activeCount > 0 && (
                <span className="filter-badge">{filters.activeCount}</span>
            )}
        </div>
        <div className="filter-sidebar-fields">
            <FilterFields filters={filters} />
        </div>
    </aside>
);

export default FilterSidebar;
