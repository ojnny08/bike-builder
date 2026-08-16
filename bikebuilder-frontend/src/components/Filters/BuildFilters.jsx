import { useEffect, useState } from "react";
import { fetchComponentTypes, fetchComponentsByCategory } from "../../services/componentService";
import "./BuildFilters.css";

let rowSeq = 0;
const newRow = () => ({ key: ++rowSeq, type: "", componentId: "" });

// Lets the viewer stack any number of "must contain this part" filters.
// Each row is a type dropdown → component dropdown; the chosen component ids
// are lifted to the parent, which refetches builds with them.
const BuildFilters = ({ onChange }) => {
    const [rows, setRows] = useState([newRow()]);
    const [types, setTypes] = useState([]);
    const [optionsByType, setOptionsByType] = useState({});   // type → components[]

    useEffect(() => {
        fetchComponentTypes().then(setTypes).catch(err => console.log(err));
    }, []);

    // Notify the parent whenever the set of chosen components changes.
    useEffect(() => {
        onChange(rows.map(r => r.componentId).filter(Boolean));
    }, [rows, onChange]);

    const loadOptions = (type) => {
        if (!type || optionsByType[type]) return;
        fetchComponentsByCategory(type)
            .then(data => setOptionsByType(prev => ({ ...prev, [type]: data.results ?? data })))
            .catch(err => console.log(err));
    };

    const setRow = (key, patch) =>
        setRows(prev => prev.map(r => (r.key === key ? { ...r, ...patch } : r)));

    const changeType = (key, type) => {
        setRow(key, { type, componentId: "" });   // component list is type-scoped, so reset it
        loadOptions(type);
    };

    const addRow = () => setRows(prev => [...prev, newRow()]);

    const removeRow = (key) =>
        setRows(prev => (prev.length === 1 ? [newRow()] : prev.filter(r => r.key !== key)));

    return (
        <div className="build-filters" aria-label="Filter builds by parts">
            <span className="filter-label">Filter by parts</span>

            {rows.map(row => (
                <div className="build-filter-row" key={row.key}>
                    <select
                        className="filter-select"
                        value={row.type}
                        onChange={e => changeType(row.key, e.target.value)}
                    >
                        <option value="">Any type</option>
                        {types.map(t => (
                            <option key={t.value} value={t.value}>{t.label}</option>
                        ))}
                    </select>

                    <select
                        className="filter-select"
                        value={row.componentId}
                        disabled={!row.type}
                        onChange={e => setRow(row.key, { componentId: e.target.value })}
                    >
                        <option value="">{row.type ? "Any component" : "Pick a type first"}</option>
                        {(optionsByType[row.type] ?? []).map(c => (
                            <option key={c.id} value={c.id}>{c.brand} {c.name}</option>
                        ))}
                    </select>

                    <button
                        type="button"
                        className="filter-clear"
                        onClick={() => removeRow(row.key)}
                        aria-label="Remove filter"
                    >
                        ×
                    </button>
                </div>
            ))}

            <button type="button" className="filter-clear" onClick={addRow}>
                + Add Filter
            </button>
        </div>
    );
};

export default BuildFilters;
