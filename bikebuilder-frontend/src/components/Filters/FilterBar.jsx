import { Fragment, useState } from "react";
import "../../styles/components/Filters/FilterBar.css";
import FilterFields from "./FilterFields";

const FilterBar = ({ filters, children, panel, searchPlaceholder = "Search products...", iconOnly = false, centered = false, floating = false, className = "" }) => {
    const { search, setSearch, activeCount } = filters;
    const [open, setOpen] = useState(false);

    const toolbarClass = [
        "filter-bar",
        centered && "filter-bar--centered",
        className,
    ].filter(Boolean).join(" ");

    const Wrapper = floating ? "div" : Fragment;
    const wrapperProps = floating ? { className: "filter-bar-wrap" } : {};

    return (
        <Wrapper {...wrapperProps}>
            <div className={toolbarClass}>
                <div className="filter-search">
                    <svg className="filter-search-icon" viewBox="0 0 24 24" aria-hidden="true">
                        <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
                        <path d="M16.5 16.5L21 21" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                    <input
                        id="filter-search"
                        type="search"
                        className="filter-search-input"
                        placeholder={searchPlaceholder}
                        value={search}
                        onChange={e => setSearch(e.target.value)}
                    />
                </div>

                {children}

                <button
                    type="button"
                    className={`filter-toggle${open ? " is-open" : ""}${iconOnly ? " filter-toggle--icon" : ""}`}
                    aria-expanded={open}
                    aria-label={iconOnly ? "Filter" : undefined}
                    onClick={() => setOpen(o => !o)}
                >
                    <svg viewBox="0 0 24 24" aria-hidden="true">
                        <path
                            d="M4 6h16M7 12h10M10 18h4"
                            stroke="currentColor" strokeWidth="2" strokeLinecap="round"
                        />
                    </svg>
                    {!iconOnly && "Filter"}
                    {activeCount > 0 && <span className="filter-badge">{activeCount}</span>}
                </button>
            </div>

            {open && (
                <div
                    className={`filter-panel${floating ? " filter-panel--floating" : ""}`}
                    role="region"
                    aria-label="Filters"
                >
                    {panel ?? <FilterFields filters={filters} />}
                </div>
            )}
        </Wrapper>
    );
};

export default FilterBar;
