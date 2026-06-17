import "./style/Builds.css";

const fmt = str => str.replace(/_/g, " ").replace(/\b\w/g, c => c.toUpperCase());

const ProgressBar = ({ steps, currentStep, selectedByCategory, onStepClick }) => {
    return (
        <div className="progress-bar-container">
            <div className="progress-steps">
                {steps.map((type, i) => {
                    const isFilled = !!selectedByCategory[type];
                    const isActive = i === currentStep;
                    const isPast = i < currentStep;
                    const isFirst = i === 0;
                    const isLast = i === steps.length - 1;
                    return (
                        <button
                            key={type}
                            className={`progress-step${isActive ? " active" : ""}${isFilled ? " filled" : ""}${isPast ? " past" : ""}${isFirst ? " first" : ""}${isLast ? " last" : ""}`}
                            onClick={() => onStepClick(i)}
                            style={{ zIndex: steps.length - i }}
                        >
                            <span className="step-label">{fmt(type)}</span>
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default ProgressBar;
