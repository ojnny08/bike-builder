import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchCurrentPublicProfile } from "../../services/userService";
import "./Profile.css";

const Profile = () => {
    const { pk } = useParams();
    const [profile, setProfile] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        fetchCurrentPublicProfile(pk)
            .then(data => setProfile(data))
            .finally(() => setLoading(false));
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
                        {profile.display_name?.[0]?.toUpperCase() ?? "?"}
                    </div>
                )}
                <h2 className="profile-name">{profile.display_name}</h2>
            </div>
        </div>
    );
};

export default Profile;
