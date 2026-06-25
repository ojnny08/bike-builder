import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import "./style/PublicBuilds.css";

const PublicBuilds = () => {
    const [buildsList, setBuildsList] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchPublicBuilds({ status: 'complete' })
            .then(data => setBuildsList(data))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="public-builds-page">
            <div className="public-builds-header">
                <div>
                    <h2 className="public-builds-title">Completed Builds</h2>
                    <p className="public-builds-subtitle">{buildsList.length} build{buildsList.length !== 1 ? "s" : ""}</p>
                </div>
                <Link to="/builds/new" className="new-build-btn">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
                    New Build
                </Link>
            </div>

            {loading ? (
                <p className="loading-text">Loading...</p>
            ) : buildsList.length === 0 ? (
                <p className="loading-text">No completed builds yet.</p>
            ) : (
                <div className="builds-grid">
                    {buildsList.map(build => (
                        <BuildsCard
                            key={build.id}
                            build={build}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default PublicBuilds;
