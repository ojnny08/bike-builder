import CategoryIcon from "../../../components/Icons/CategoryIcons";
import "../../../styles/pages/Builds/Builds.css";

const stepTitle = step => {
    if (step.skipped) return `${step.label} (N/A)`;
    if (step.unknown) return `${step.label} (unknown)`;
    return step.label;
};

const ProgressSteps = ({ steps = [], focused, onFocus }) => (
    <div className="bs-steps">
        {steps.map(step => (
            <button
                key={step.key}
                type="button"
                className={`bs-step${step.filled ? " is-filled" : ""}${focused === step.key ? " is-focused" : ""}${step.locked ? " is-locked" : ""}${step.skipped ? " is-skipped" : ""}${step.unknown ? " is-unknown" : ""}`}
                disabled={step.locked}
                aria-current={focused === step.key ? "step" : undefined}
                aria-label={stepTitle(step)}
                title={stepTitle(step)}
                onClick={() => onFocus(step.key)}
            >
                <span className="bs-step-icon"><CategoryIcon category={step.key} /></span>
            </button>
        ))}
    </div>
);

export default ProgressSteps;
