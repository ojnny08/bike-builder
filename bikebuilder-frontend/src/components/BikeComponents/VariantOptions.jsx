import { useEffect, useMemo, useState } from "react";
import "./VariantModal.css";

const titleCase = v => String(v).replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

const ATTR_META = {
    bb_type: { label: "threading", format: v => String(v).toUpperCase() },
    color: { label: "colour", format: v => v },
    length_mm: { label: "length", format: v => v },
    chainring_teeth: { label: "teeth", format: v => `${v}T` },
    hole_count: { label: "spoke holes", format: v => `${v}h` },
    cog_interface: { label: "drive", format: titleCase },
};

const metaFor = key => ATTR_META[key] || { label: key, format: v => String(v) };

const isBlank = v => v === "" || v === null || v === undefined;

export const attributeKeys = options => {
    if (!options?.length) return [];
    return Object.keys(options[0])
        .filter(k => k !== "id" && k !== "price")
        .filter(k => options.some(o => !isBlank(o[k])));
};

export const hasVariants = options => attributeKeys(options).length > 0;

const distinctValues = (options, key) => [...new Set(options.map(o => o[key]))];

const matches = (option, selected, keys) =>
    keys.every(k => String(option[k]) === String(selected[k]));

const VariantOptions = ({ options = [], onResolve }) => {
    const keys = useMemo(() => attributeKeys(options), [options]);

    const [selected, setSelected] = useState(() =>
        options[0] ? Object.fromEntries(keys.map(k => [k, options[0][k]])) : {}
    );

    const resolved = keys.length
        ? options.find(o => matches(o, selected, keys)) ?? null
        : options[0] ?? null;

    useEffect(() => {
        onResolve?.(resolved);
    }, [resolved?.id]);

    if (!keys.length) return null;

    const isAvailable = (key, value) => {
        const others = keys.filter(k => k !== key);
        return options.some(
            o => String(o[key]) === String(value) && matches(o, selected, others)
        );
    };

    return (
        <div className="variant-options">
            {keys.map(key => (
                <label key={key} className="variant-field">
                    <span className="variant-field-label">{metaFor(key).label}</span>
                    <select
                        className="variant-select"
                        value={selected[key]}
                        onChange={e => setSelected(s => ({ ...s, [key]: e.target.value }))}
                    >
                        {distinctValues(options, key).map(value => {
                            const available = isAvailable(key, value);
                            return (
                                <option key={value} value={value} disabled={!available}>
                                    {metaFor(key).format(value)}{!available ? " (unavailable)" : ""}
                                </option>
                            );
                        })}
                    </select>
                </label>
            ))}
        </div>
    );
};

export default VariantOptions;
