import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";

// Dedicated top bar for the builder flow. Replaces the site navbar so the
// screen stays focused on building: brand, progress, start over, save.
const BuilderNav = ({ onSave, saveLabel = "Save build", hideSave = false }) => {
    const { build, emptyBuild } = useBuild();
    const navigate = useNavigate();

    const { required = [] } = build.bikeType?.rules ?? {};
    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );
    const requiredFilled = required.filter(t => selectedByCategory[t]).length;

    const handleStartOver = () => {
        emptyBuild();
        navigate("/builds/new");
    };

    const handleSave = onSave ?? (() => navigate("/builds/new/review"));

    return (
        <header className="bn-bar">
            <button className="bn-brand" onClick={() => navigate("/")}>
                <svg className="bn-brand-icon" width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                    <circle cx="18.5" cy="17.5" r="3.5" />
                    <circle cx="5.5" cy="17.5" r="3.5" />
                    <circle cx="15" cy="5" r="1" />
                    <path d="M12 17.5V14l-3-3 4-3 2 3h2" />
                </svg>
                Bikco
            </button>

            <div className="bn-info">
                <span className="bn-type-name">{build.bikeType?.name}</span>
                <span className="bn-count">{requiredFilled}/{required.length}</span>
            </div>

            <div className="bn-actions">
                <button className="bb-btn-ghost" onClick={handleStartOver}>Start over</button>
                {!hideSave && (
                    <button
                        className="bb-btn-primary"
                        onClick={handleSave}
                        disabled={build.components.length === 0}
                    >
                        {saveLabel}
                    </button>
                )}
            </div>
        </header>
    );
};

export default BuilderNav;
