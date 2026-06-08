import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useBuild } from "../../context/BuildContext";
import { fetchBuilds, deleteBuild, getBuild } from "../../services/buildService";
import "./PublicBuilds.css";

const PublicBuilds = () => {
    const [buildsList, setBuildsList] = useState([]);
    const [loading, setLoading] = useState(true);
    const { editBuild } = useBuild();
    const navigate = useNavigate();

    useEffect(() => {
        fetchBuilds()
            .then(data => setBuildsList(data))
            .finally(() => setLoading(false));
    }, []);

    const handleDelete = async (pk) => {
        try {
            await deleteBuild(pk);
            setBuildsList(prev => prev.filter(b => b.id !== pk));
        } catch (error) {
            console.log(error);
        }
    };

    const handleEdit = async (pk) => {
        try {
            const data = await getBuild(pk);
            editBuild({ build: data });
            navigate("/builds/new");
        } catch (error) {
            console.log(error);
        }
    };

    return (
        <div className="public-builds-page">
            <div className="public-builds-header">
                <div>
                    <h2 className="public-builds-title">My Builds</h2>
                    <p className="public-builds-subtitle">{buildsList.length} build{buildsList.length !== 1 ? "s" : ""}</p>
                </div>
                <Link to="/builds/new" className="new-build-btn">New Build</Link>
            </div>

            {loading ? (
                <p className="loading-text">Loading...</p>
            ) : buildsList.length === 0 ? (
                <div className="empty-builds">
                    <p>You haven't saved any builds yet.</p>
                    <Link to="/builds/new" className="new-build-btn">Start your first build</Link>
                </div>
            ) : (
                <div className="builds-grid">
                    {buildsList.map(build => (
                        <div key={build.id} className="build-card">
                            <div className="build-card-header">
                                <span className="build-bike-type">{build.name}</span>
                                <span className={`build-status ${build.status}`}>{build.status.replace("_", " ")}</span>
                            </div>
                            <p className="build-component-count">{build.components.length} components</p>
                            <p className="build-date">{new Date(build.created_at).toLocaleDateString()}</p>
                            <button className="delete-btn" onClick={() => handleDelete(build.id)}>Delete</button>
                            <button className="delete-btn" onClick={() => handleEdit(build.id)}>Edit</button>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default PublicBuilds;
