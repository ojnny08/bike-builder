import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { getSharedBuild } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import Comments from "../../components/Comments/Comments";
import "./style/PublicBuilds.css";

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

    return (
        <div className="public-builds-page">
            <div className="public-builds-header">
                <div>
                    <h2 className="public-builds-title">{build.name}</h2>
                    <p className="public-builds-subtitle">by {build.user.display_name}</p>
                </div>
                <Link to="/builds" className="new-build-btn">Browse Builds</Link>
            </div>

            <div className="builds-grid">
                <BuildsCard build={build} />
            </div>

            <Comments buildId={build.id} />
        </div>
    );
};

export default BuildDetail;
