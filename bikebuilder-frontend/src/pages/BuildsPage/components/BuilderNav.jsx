import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import "../style/Builds.css";

// Dedicated top bar for the builder flow. Replaces the site navbar so the
// screen stays focused on building: brand, progress, start over, save.
const BuilderNav = () => {
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

    return (
        <>
            <div className="bs-topbar-side">
                <button className="bb-btn-ghost" onClick={() => navigate(-1)}>←</button>
                <button className="bb-btn-ghost" onClick={() => navigate("/")}>Home</button>
                <button className="bb-btn-ghost" onClick={handleStartOver}>Start over</button>
                <button
                    className="bb-btn-primary"
                    onClick={() => navigate("/builds/new/review")}
                >
                    Save progress
                </button>
            </div>
        </>
    );
};

export default BuilderNav;
