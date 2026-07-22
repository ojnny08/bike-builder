import "../style/Builds.css";

const ProgressBar = ({ progress = 0, filled = 0, total = 0 }) => (
    <div className="bb-progress" aria-label={`${filled} of ${total} essential parts selected`}>
        <span className="bb-bar-track">
            <span className="bb-bar-fill" style={{ transform: `scaleX(${progress})` }} />
        </span>
    </div>
);

export default ProgressBar;
