import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getSharedBuild } from "../../services/buildService";
import Comments from "../../components/Comments/Comments";
import { titleCase, money, sumPrice } from "../../utils/format";
import "./BuildDetail.css";

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

    const totalPrice = sumPrice(build.components);

    return (
        <div className="page build-detail-page">
            <div className="build-view">
                <div className="build-view-heading">
                        <Link to="/builds" className="build-view-browse">Browse builds</Link>
                    </div>
                <div className="build-view-main">

                    <div className="build-view-photo">
                        {build.image_url
                            ? <img src={build.image_url} alt={build.name} className="build-view-img" />
                            : <div className="build-view-img-placeholder">No photo</div>
                        }
                    </div>

                    {build.description && (
                        <div className="build-view-description">
                            <h2 className="build-view-name">{build.name}</h2>
                            <p className="build-view-author">by {build.user.display_name}</p>
                            <p className="build-view-description-text">{build.description}</p>
                        </div>
                    )}

                    <div className="build-view-comments">
                        <Comments buildId={build.id} />
                    </div>
                </div>

                <div className="build-view-specs">
                    <h3 className="build-view-section-title">Components</h3>
                    <ul className="build-view-components">
                        {build.components.map(c => (
                            <li key={c.id} className="build-view-component">
                                <span className="build-view-part-cat">{titleCase(c.component_type)}</span>
                                <span className="build-view-part-name">
                                    {c.name}
                                    {c.brand && <span className="build-view-part-brand"> · {c.brand}</span>}
                                </span>
                                <span className="build-view-part-price">
                                    {c.price ? money(c.price) : '—'}
                                </span>
                            </li>
                        ))}
                    </ul>
                    <div className="build-view-total">
                        <span>Total</span>
                        <span className="build-view-total-price">{money(totalPrice)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default BuildDetail;
