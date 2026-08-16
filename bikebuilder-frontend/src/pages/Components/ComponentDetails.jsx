import { useParams, useNavigate } from "react-router-dom";
import ComponentDetailView from "../../components/BikeComponents/ComponentDetailView";
import "./ComponentDetails.css";

const ComponentDetails = () => {
    const { id, category, group, mode } = useParams();
    const navigate = useNavigate();
    const inBuildFlow = Boolean(category || group);

    const onAdded = () => navigate(group ? `/builds/new/select-group/${group}/${mode}` : "/builds/new");

    return (
        <div className="page comp-detail-page">
            <div className="comp-view-heading">
                <button type="button" className="comp-view-back" onClick={() => navigate(-1)}>
                    Back
                </button>
            </div>
            <ComponentDetailView id={id} inBuildFlow={inBuildFlow} onAdded={onAdded} />
        </div>
    );
};

export default ComponentDetails;
