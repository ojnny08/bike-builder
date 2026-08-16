import { useNavigate, useParams } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import ProgressBar from "./ProgressBar";
import "../Builds.css";

// Dedicated top bar for the builder flow. Replaces the site navbar so the
// screen stays focused on building: brand, progress, start over, save.
const BuilderNav = ({ hideSave = false, stage = false }) => {
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

    const showControls = !hideSave && required.length > 0;

    const back = <button className="bb-btn-back" onClick={() => navigate(-1)}>←</button>;
    const progressBar = (
        <ProgressBar progress={progress} filled={requiredFilled} total={required.length} />
    );
    const controls = (
        <>
            <button className="bb-btn-ghost" onClick={() => navigate("/")}>Home</button>
            <button className="bb-btn-ghost" onClick={handleStartOver}>Start Over</button>
            <button className="bb-btn-primary" onClick={() => navigate("/builds/new/review")}>
                Save Progress
            </button>
        </>
    );

    if (stage) {
        return (
            <div className="bs-topbar bs-topbar--stage">
                <div className="bs-topbar-canvas">
                    <div className="bs-topbar-back">{back}</div>
                    {showControls && <div className="bs-topbar-progress">{progressBar}</div>}
                </div>
                <div className="bs-topbar-panel">
                    {showControls && controls}
                </div>
            </div>
        );
    }

    return (
        <div className="bs-topbar">
            <div className="bs-topbar-left">{back}</div>

            {showControls && (
                <div className="bs-topbar-center">{progressBar}</div>
            )}
            {showControls && (
                <div className="bs-topbar-right">{controls}</div>
            )}
        </div>
    );
};

export default BuilderNav;
