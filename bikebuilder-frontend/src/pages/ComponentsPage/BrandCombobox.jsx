import { useState, useRef, useEffect } from "react";

// Searchable brand dropdown: type to filter the list, click to select.
// `value` is the applied brand (""=all); `onChange` reports the picked brand.
const BrandCombobox = ({ brands, value, onChange }) => {
    const [query, setQuery] = useState("");
    const [open, setOpen] = useState(false);
    const ref = useRef(null);

    // Close the dropdown when clicking anywhere outside it.
    useEffect(() => {
        const onClickOutside = (e) => {
            if (ref.current && !ref.current.contains(e.target)) setOpen(false);
        };
        document.addEventListener("mousedown", onClickOutside);
        return () => document.removeEventListener("mousedown", onClickOutside);
    }, []);

    const filtered = query
        ? brands.filter(b => b.toLowerCase().includes(query.toLowerCase()))
        : brands;

    const select = (brand) => {
        onChange(brand);
        setQuery("");
        setOpen(false);
    };

    return (
        <div className="combobox" ref={ref}>
            <input
                type="text"
                className="filter-input"
                role="combobox"
                aria-expanded={open}
                aria-controls="brand-listbox"
                placeholder={value || "All brands"}
                value={query}
                onChange={e => { setQuery(e.target.value); setOpen(true); }}
                onFocus={() => setOpen(true)}
                onKeyDown={e => e.key === "Escape" && setOpen(false)}
            />

            {open && (
                <ul className="combobox-list" id="brand-listbox" role="listbox">
                    <li
                        role="option"
                        aria-selected={value === ""}
                        className={`combobox-option${value === "" ? " is-selected" : ""}`}
                        onMouseDown={() => select("")}
                    >
                        All brands
                    </li>
                    {filtered.map(b => (
                        <li
                            key={b}
                            role="option"
                            aria-selected={value === b}
                            className={`combobox-option${value === b ? " is-selected" : ""}`}
                            onMouseDown={() => select(b)}
                        >
                            {b}
                        </li>
                    ))}
                    {filtered.length === 0 && (
                        <li className="combobox-empty">No brands match</li>
                    )}
                </ul>
            )}
        </div>
    );
};

export default BrandCombobox;
