import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useBuild } from "../../context/BuildContext";
import { fetchBuilds, deleteBuild, getBuild } from "../../services/buildService";
import PublicBuildsCard from "../../components/Builds/BuildsCard";
import "./style/PublicBuilds.css";

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
                        <PublicBuildsCard 
                            key={build.id}
                            build={build}
                            onDelete={handleDelete}
                            onEdit={handleEdit}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default PublicBuilds;
