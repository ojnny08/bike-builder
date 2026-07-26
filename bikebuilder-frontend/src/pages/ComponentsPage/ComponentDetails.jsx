import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchComponentDetails } from "../../services/componentService";
import "./ComponentDetails.css";

const ComponentDetails = () => {
    const { id } = useParams();
    const navigate = useNavigate();
    const [comp, setComp] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        setLoading(true);
        setError(false);
        fetchComponentDetails(id)
            .then(setComp)
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, [id]);

    if (loading) return <div className="page detail-page detail-state">Loading...</div>;
    if (error || !comp) return <div className="page detail-page detail-state">Component not found</div>;

    return (
        <div className="page detail-page">
            <button type="button" className="detail-back" onClick={() => navigate(-1)}>
                Back
            </button>

            <div className="detail-layout">
                <div className="detail-media">
                    {comp.image_url && <img src={comp.image_url} alt={comp.name} />}
                </div>

                <div className="detail-info">
                    <span className="detail-type">{comp.component_type?.replace(/_/g, " ")}</span>
                    <h1 className="detail-brand">{comp.brand}</h1>
                    <p className="detail-name">{comp.name}</p>

                    <div className="detail-meta">
                        <span className="detail-price">${comp.price}</span>
                        <span className="detail-weight">{comp.weight_grams}g</span>
                    </div>

                    {comp.import_url && (
                        <a className="detail-link" href={comp.import_url} target="_blank" rel="noreferrer">
                            View at retailer
                        </a>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ComponentDetails;
