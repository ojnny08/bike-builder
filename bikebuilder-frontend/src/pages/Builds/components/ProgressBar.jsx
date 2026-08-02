import "../style/Builds.css";

const ProgressBar = ({ progress = 0, filled = 0, total = 0 }) => {

    return (
    <div className="bb-progress">
        <span className="bb-bar-track">
            <span className="bb-bar-fill" style={{ transform: `scaleX(${progress})` }} />
        </span>
        <span className="bb-progress-count">{filled}/{total}</span>
    </div>
    )
};

export default ProgressBar;
