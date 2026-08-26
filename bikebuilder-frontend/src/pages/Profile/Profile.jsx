import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchCurrentPublicProfile } from "../../services/userService";
import { fetchPublicBuilds, getBuild, deleteBuild, uploadBuildImage } from "../../services/buildService";
import { useBuild } from "../../context/BuildContext";
import BuildsCard from "../../components/Builds/BuildsCard";
import "../../styles/pages/Profile/Profile.css";

const Profile = () => {
    const { username } = useParams();
    const [profile, setProfile] = useState(null);
    const [buildsList, setBuildsList] = useState([]);
    const { editBuild } = useBuild();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        Promise.all([
            fetchCurrentPublicProfile(username),
            fetchPublicBuilds({ username }),
        ]).then(([profileData, buildsData]) => {
            setProfile(profileData);
            setBuildsList(buildsData);
        }).finally(() => setLoading(false));
    }, [username]);

    const handleEdit = async (id) => {
        try {
            const data = await getBuild(id);
            editBuild({ build: data });
            navigate("/builds/new");
        } catch (error) {
            console.log(error);
        }
    };

    const handleDelete = async (id) => {
        try {
            await deleteBuild(id);
            setBuildsList(prev => prev.filter(b => b.id !== id));
        } catch (error) {
            console.log(error);
        }
    }

    const handleUploadImage = async (id, file) => {
        const url = await uploadBuildImage(id, file);
        setBuildsList(prev => prev.map(b => b.id === id ? { ...b, image_url: url } : b));
    };

    if (loading) return <p className="loading-text">Loading...</p>;
    if (!profile) return <p className="loading-text">Profile not found.</p>;

    return (
        <div className="page profile-page">
            <div className="profile-view">
                <div className="profile-body">
                    <aside className="profile-side">
                        <div className="profile-header">
                            {profile.photo_url ? (
                                <img className="profile-avatar" src={profile.photo_url} alt={profile.display_name} />
                            ) : (
                                <div className="profile-avatar-placeholder">
                                    {profile.display_name?.[0] ?? "?"}
                                </div>
                            )}
                            <span className="profile-name">{profile.display_name}</span>
                        </div>
                        <section className="profile-section">
                            <h2 className="profile-section-label">About me</h2>
                            <p className="profile-section-empty">Nothing here yet.</p>
                        </section>
                        <section className="profile-section">
                            <h2 className="profile-section-label">Gear ratio</h2>
                            <p className="profile-section-empty">Nothing here yet.</p>
                        </section>
                        <section className="profile-section">
                            <h2 className="profile-section-label">Socials</h2>
                            <p className="profile-section-empty">Nothing here yet.</p>
                        </section>
                    </aside>

                    <div className="profile-builds">
                        <div className="profile-builds-head">
                            <h2 className="profile-builds-title">Bikes</h2>
                        </div>

                        {buildsList.length === 0 ? (
                            <p className="profile-builds-empty">No builds shared yet.</p>
                        ) : (
                            <div className="profile-build-card">
                                {buildsList.map((build) => (
                                    <BuildsCard
                                        key={build.id}
                                        build={build}
                                        onDelete={handleDelete}
                                        onEdit={handleEdit}
                                        onUploadImage={handleUploadImage} />
                                ))}
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Profile;
