import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchCurrentPublicProfile } from "../../services/userService";
import { fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import { getBuild } from "../../services/buildService";
import { useBuild } from "../../context/BuildContext";
import { useNavigate } from "react-router-dom";
import "./Profile.css";

const Profile = () => {
    const { pk } = useParams();
    const [profile, setProfile] = useState(null);
    const [buildsList, setBuildsList] = useState([]);
    const { editBuild } = useBuild();
    const navigate = useNavigate('');
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        Promise.all([
            fetchCurrentPublicProfile(pk),
            fetchPublicBuilds({ user: pk }),
        ]).then(([profileData, buildsData]) => {
            setProfile(profileData);
            setBuildsList(buildsData);
        }).finally(() => setLoading(false));
    }, [pk]);

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

    if (loading) return <p className="loading-text">Loading...</p>;
    if (!profile) return <p className="loading-text">Profile not found.</p>;

    return (
        <div className="profile-page">
            <div className="profile-header">
                {profile.photo_url ? (
                    <img className="profile-avatar" src={profile.photo_url} alt={profile.display_name} />
                ) : (
                    <div className="profile-avatar-placeholder">
                        {profile.display_name ?? "?"}
                    </div>
                )}
                <h2 className="profile-name">{profile.display_name}</h2>
            </div>
            
            <div className="profile-build-card">
                {buildsList.map((build) => (
                    <BuildsCard
                        key={build.id}
                        build={build}
                        onDelete={handleDelete}
                        onEdit={handleEdit}/>
                ))}
            </div>
        </div>
    );
};

export default Profile;
