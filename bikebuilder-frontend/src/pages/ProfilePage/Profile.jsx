import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchCurrentPublicProfile } from "../../services/userService";
import { fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import "./Profile.css";

const Profile = () => {
    const { pk } = useParams();
    const [profile, setProfile] = useState(null);
    const [buildsList, setBuildsList] = useState([]);
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
                        build={build}/>
                ))}
            </div>
        </div>
    );
};

export default Profile;
