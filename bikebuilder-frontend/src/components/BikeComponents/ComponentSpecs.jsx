const BASE_KEYS = new Set([
    "id", "component_type", "name", "brand", "weight_grams", "price",
    "image_url", "import_url", "options", "description", "compatible", "selectedOption",
]);

const UNIT_BY_KEY = {
    sprocket_teeth: "T",
    chainring_teeth: "T",
    seatpost_size: "mm",
    hole_count: "h",
};

const isBlank = v => v === null || v === undefined || v === "";

const isNumeric = s => s !== "" && !Number.isNaN(Number(s));

const labelFor = key =>
    key.replace(/_(mm|degrees)$/, "").replace(/_/g, " ").replace(/^\w/, c => c.toUpperCase());

const formatValue = (key, v) => {
    if (typeof v === "boolean") return v ? "yes" : "no";
    const s = String(v);
    if (key === "wheel_size" && /^\d+(\.\d+)?$/.test(s)) return `${s}"`;
    if (UNIT_BY_KEY[key] && isNumeric(s)) return `${s}${UNIT_BY_KEY[key]}`;
    if (key.endsWith("_mm") && isNumeric(s)) return `${s}mm`;
    if (key.endsWith("_degrees") && isNumeric(s)) return `${s}°`;
    return s.replace(/_/g, " ");
};

const ComponentSpecs = ({ component }) => {
    const rows = Object.entries(component)
        .filter(([k, v]) => !BASE_KEYS.has(k) && typeof v !== "object" && !isBlank(v))
        .map(([k, v]) => [labelFor(k), formatValue(k, v)]);

    if (!rows.length) return null;

    return (
        <dl className="variant-specs">
            {rows.map(([label, value]) => (
                <div key={label} className="variant-spec">
                    <dt>{label}</dt>
                    <dd>{value}</dd>
                </div>
            ))}
        </dl>
    );
};

export default ComponentSpecs;
