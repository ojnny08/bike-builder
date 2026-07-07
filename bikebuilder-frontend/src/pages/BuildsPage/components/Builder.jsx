import { Fragment } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import BuilderNav from "./BuilderNav";
import "../style/Builds.css";

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const money = n => `$${n.toFixed(2)}`;

// Order the part selection into meaningful groups. Only categories the current
// bike type actually uses are shown; anything not listed here falls into a
// trailing "More" group so nothing is dropped.
const PART_GROUPS = [
    { label: "Frame & drivetrain", cats: ["frame", "bottom_bracket", "crankset", "wheel"] },
    { label: "Gearing & tires", cats: ["chainring", "sprocket", "chain", "tire"] },
    { label: "Saddle", cats: ["seatpost", "saddle"] },
    { label: "Cockpit", cats: ["stem", "brake", "handlebar"] },
    { label: "Pedals", cats: ["pedals"] },
];

const PartGlyph = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4"
        strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="3.2" />
        <path d="M12 2.6v3M12 18.4v3M2.6 12h3M18.4 12h3M5.4 5.4l2.1 2.1M16.5 16.5l2.1 2.1M18.6 5.4l-2.1 2.1M7.5 16.5l-2.1 2.1" />
    </svg>
);

const Thumb = ({ src }) => (
    <span className="bb-thumb">
        {src ? <img src={src} alt="" loading="lazy" /> : <span className="bb-thumb-glyph"><PartGlyph /></span>}
    </span>
);

const PartRow = ({ category, selected, locked, prereq, onChoose }) => (
    <div
        className={`bb-row${locked ? ' is-locked' : ''}${selected ? ' is-filled' : ''}`}
        role="button"
        tabIndex={locked ? -1 : 0}
        aria-disabled={locked}
        onClick={() => !locked && onChoose()}
        onKeyDown={e => { if (!locked && (e.key === 'Enter' || e.key === ' ')) { e.preventDefault(); onChoose(); } }}
    >
        <Thumb src={selected?.image_url} />
        <div className="bb-row-main">
            <span className="bb-row-cat">{formatCat(category)}</span>
            {selected ? (
                <span className="bb-row-name">{selected.name}<span className="bb-row-brand"> · {selected.brand}</span></span>
            ) : locked ? (
                <span className="bb-row-msg">Select {formatCat(prereq)} first</span>
            ) : (
                <span className="bb-row-placeholder">Choose a {formatCat(category).toLowerCase()}</span>
            )}
        </div>
        <span className="bb-row-price">{selected?.price ? money(parseFloat(selected.price)) : '—'}</span>
        <span className="bb-row-action">{selected ? 'Change' : locked ? '' : 'Add'}</span>
    </div>
);

const Builder = () => {
    const { build } = useBuild();
    const { required = [], optional = [], prerequisites = {} } = build.bikeType.rules;
    const navigate = useNavigate();

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const isLocked = (category) => {
        const dep = prerequisites[category];
        return dep && [...required, ...optional].includes(dep) && !selectedByCategory[dep];
    };

    const requiredFilled = required.filter(t => selectedByCategory[t]).length;
    const allRequiredFilled = required.length > 0 && requiredFilled === required.length;

    // Group the bike type's categories per PART_GROUPS, keeping only categories
    // this bike type uses and appending any uncovered ones under "More".
    const allCategories = [...required, ...optional];
    const grouped = PART_GROUPS
        .map(g => ({ label: g.label, cats: g.cats.filter(c => allCategories.includes(c)) }))
        .filter(g => g.cats.length > 0);
    const covered = new Set(grouped.flatMap(g => g.cats));
    const leftover = allCategories.filter(c => !covered.has(c));
    const partGroups = leftover.length > 0
        ? [...grouped, { label: "More", cats: leftover }]
        : grouped;
    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight_grams) || 0), 0);

    return (
        <div className="bb-wrapper">
            <BuilderNav onSave={() => navigate("/builds/new/review")} />
            <div className="bb-main">
                <div className="bb-topbar">
                    <span className="bb-build-type">{build.bikeType.name}</span>
                </div>

                <div className="bb-list">
                    {partGroups.map(group => (
                        <Fragment key={group.label}>
                            <h2 className="bb-group-label">{group.label}</h2>
                            {group.cats.map(category => (
                                <PartRow
                                    key={category}
                                    category={category}
                                    selected={selectedByCategory[category]}
                                    locked={isLocked(category)}
                                    prereq={prerequisites[category]}
                                    onChoose={() => navigate(`/builds/new/select/${category}`)}
                                />
                            ))}
                        </Fragment>
                    ))}
                </div>

                <footer className="bb-footer">
                    <div className="bb-footer-totals">
                        <span className="bb-footer-weight">{totalWeight > 0 ? `${totalWeight.toFixed(0)} g` : ''}</span>
                        <span className="bb-footer-price">{money(totalPrice)}</span>
                    </div>
                    <div className="bb-footer-cta">
                        {!allRequiredFilled && (
                            <span className="bb-footer-hint">
                                {required.length - requiredFilled} essential part{required.length - requiredFilled === 1 ? '' : 's'} left
                            </span>
                        )}
                        <button
                            className="bb-btn-primary bb-btn-lg"
                            onClick={() => navigate("/builds/new/review")}
                            disabled={build.components.length === 0}
                        >
                            Review build
                        </button>
                    </div>
                </footer>
            </div>
        </div>
    );
};

export default Builder;
