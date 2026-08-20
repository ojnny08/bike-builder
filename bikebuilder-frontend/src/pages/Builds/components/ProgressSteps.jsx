import CategoryIcon from "../../../components/Icons/CategoryIcons";
import "../Builds.css";

const ProgressSteps = ({ steps = [], focused, onFocus }) => (
    <div className="bs-steps">
        {steps.map(step => (
            <button
                key={step.key}
                type="button"
                className={`bs-step${step.filled ? " is-filled" : ""}${focused === step.key ? " is-focused" : ""}${step.locked ? " is-locked" : ""}`}
                disabled={step.locked}
                aria-current={focused === step.key ? "step" : undefined}
                aria-label={step.label}
                title={step.label}
                onClick={() => onFocus(step.key)}
            >
                <span className="bs-step-icon"><CategoryIcon category={step.key} /></span>
            </button>
        ))}
    </div>
);

export default ProgressSteps;
