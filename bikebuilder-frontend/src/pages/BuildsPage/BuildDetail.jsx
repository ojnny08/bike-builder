import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getSharedBuild } from "../../services/buildService";
import Comments from "../../components/Comments/Comments";
import "./style/PublicBuilds.css";

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

const BuildDetail = () => {
    const { token } = useParams();
    const [build, setBuild] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);

    useEffect(() => {
        getSharedBuild(token)
            .then(setBuild)
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, [token]);

    if (loading) return <p className="loading-text">Loading...</p>;
    if (error || !build) return <p className="loading-text">This build is unavailable.</p>;

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);

    return (
        <div className="public-builds-page">
            <div className="public-builds-header">
                <div>
                    <h2 className="public-builds-title">{build.name}</h2>
                    <p className="public-builds-subtitle">by {build.user.display_name}</p>
                </div>
                <Link to="/builds" className="new-build-btn">Browse Builds</Link>
            </div>

            <div className="build-view">
                <div className="build-view-main">
                    <div className="build-view-photo">
                        {build.image_url
                            ? <img src={build.image_url} alt={build.name} className="build-view-img" />
                            : <div className="build-view-img-placeholder">No photo</div>
                        }
                    </div>

                    {build.description && (
                        <div className="build-view-description">
                            <h3 className="build-view-section-title">Description</h3>
                            <p className="build-view-description-text">{build.description}</p>
                        </div>
                    )}

                    <Comments buildId={build.id} />
                </div>

                <div className="build-view-specs">
                    <h3 className="build-view-section-title">Components</h3>
                    <ul className="build-view-components">
                        {build.components.map(c => (
                            <li key={c.id} className="build-view-component">
                                <span className="build-view-comp-cat">{formatCat(c.component_type)}</span>
                                <span className="build-view-comp-name">
                                    {c.name}
                                    {c.brand && <span className="build-view-comp-brand"> · {c.brand}</span>}
                                </span>
                                <span className="build-view-comp-price">
                                    {c.price ? `$${parseFloat(c.price).toFixed(2)}` : '—'}
                                </span>
                            </li>
                        ))}
                    </ul>
                    <div className="build-view-total">
                        <span>Total</span>
                        <span className="build-view-total-price">${totalPrice.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BuildDetail;
