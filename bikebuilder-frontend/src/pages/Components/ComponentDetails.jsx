import { useParams, useNavigate } from "react-router-dom";
import ComponentDetailView from "../../components/BikeComponents/ComponentDetailView";
import "./ComponentDetails.css";

const ComponentDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();

    return (
        <div className="page comp-detail-page">
            <div className="comp-view-heading">
                <button type="button" className="comp-view-back" onClick={() => navigate(-1)}>
                    Back
                </button>
            </div>
            <ComponentDetailView id={id} />
        </div>
    );
};

export default ComponentDetails;
