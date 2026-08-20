import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import ProgressBar from "./ProgressBar";
import "../Builds.css";

const BuilderNav = ({ hideSave = false }) => {
    const { build, emptyBuild } = useBuild();
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

    const progressBar = (
        <ProgressBar progress={progress} filled={requiredFilled} total={required.length} />
    );
    const controls = (
        <>
            <button className="bb-btn-ghost" onClick={handleStartOver}>Start Over</button>
            <button className="bb-btn-primary" onClick={() => navigate("/builds/new/review")}>
                Save Progress
            </button>
        </>
    );

    return (
        <div className="bs-topbar">

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
