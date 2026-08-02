import { useNavigate, useParams } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import ProgressBar from "./ProgressBar";
import "../style/Builds.css";

// Dedicated top bar for the builder flow. Replaces the site navbar so the
// screen stays focused on building: brand, progress, start over, save.
const BuilderNav = ({ hideSave = false }) => {
    const { build, emptyBuild } = useBuild();
    const { category } = useParams();
    const navigate = useNavigate();

    const { required = [] } = build.bikeType?.rules ?? {};
    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );
    const requiredFilled = required.filter(t => selectedByCategory[t]).length;
    const progress = required.length ? requiredFilled / required.length : 0;

    const handleStartOver = () => {
        emptyBuild();
        navigate("/builds/new");
    };

    return (
        <div className="bs-topbar">
            <div className="bs-topbar-left">
                <button className="bb-btn-back" onClick={() => navigate(-1)}>←</button>
                <button className="bb-btn-ghost" onClick={() => navigate("/")}>Home</button>
            </div>

            {!hideSave && required.length > 0 && (
                <div className="bs-topbar-center">
                    <ProgressBar progress={progress} filled={requiredFilled} total={required.length} />
                </div>
            )}

            <div className="bs-topbar-right">
                <button className="bb-btn-ghost" onClick={handleStartOver}>Start Over</button>
                {!hideSave && (
                    <button
                        className="bb-btn-primary"
                        onClick={() => navigate("/builds/new/review")}
                    >
                        Save Progress
                    </button>
                )}
            </div>
        </div>
    );
};

export default BuilderNav;
