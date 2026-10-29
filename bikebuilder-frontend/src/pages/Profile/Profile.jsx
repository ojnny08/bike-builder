import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { fetchCurrentPublicProfile, fetchCurrentUserProfile, updateCurrentUserProfile } from "../../services/userService";
import { fetchPublicBuilds, getBuild, deleteBuild, uploadBuildImage } from "../../services/buildService";
import { useBuild } from "../../context/BuildContext";
import { useAuth } from "../../context/AuthContext";
import BuildsCard from "../../components/Builds/BuildsCard";
import "../../styles/pages/Profile/Profile.css";

const Profile = () => {
    const { username } = useParams();
    const [profile, setProfile] = useState(null);
    const [isEditing, setIsEditing] = useState(false);
    const [form, setForm] = useState({ display_name: "", bio: "" });
    const [saving, setSaving] = useState(false);
    const [saveError, setSaveError] = useState("");
    const [buildsList, setBuildsList] = useState([]);
    const [myUsername, setMyUsername] = useState(null);
    const { editBuild } = useBuild();
    const { currentUser, loading: authLoading } = useAuth();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (authLoading) return;
        Promise.all([
            fetchCurrentPublicProfile(username),
            fetchPublicBuilds({ username }),
        ]).then(([profileData, buildsData]) => {
            setProfile(profileData);
            setBuildsList(buildsData);
        }).finally(() => setLoading(false));
    }, [username, authLoading]);

    useEffect(() => {
        if (!currentUser) return;
        let active = true;
        fetchCurrentUserProfile()
            .then((me) => { if (active) setMyUsername(me.username); })
            .catch(() => {});
        return () => { active = false; };
    }, [currentUser]);

    const isOwner = Boolean(currentUser) && myUsername === username;

    const handleEdit = async (id) => {
        try {
            const data = await getBuild(id);
            editBuild({ build: data });
            navigate("/builds/new");
        } catch (error) {
            console.log(error);
        }
    };

    const openEditProfile = () => {
        setForm({ display_name: profile.display_name ?? "", bio: profile.bio ?? "" });
        setSaveError("");
        setIsEditing(true);
    };

    const handleEditProfile = async (e) => {
        e.preventDefault();
        setSaving(true);
        setSaveError("");
        try {
            const updated = await updateCurrentUserProfile(form);
            setProfile((prev) => ({ ...prev, display_name: updated.display_name, bio: updated.bio }));
            setIsEditing(false);
        } catch {
            setSaveError("Could not save your changes. Please try again.");
        } finally {
            setSaving(false);
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

    if (isEditing) return (
        <div className="page profile-page">
            <div className="profile-edit">
                <header className="profile-edit-head">
                    <h1 className="profile-edit-title">Edit profile</h1>
                    <p className="profile-edit-note">
                        Information added here is visible to anyone who views your profile. Keep personal details private.
                    </p>
                </header>

                <form className="profile-edit-form" onSubmit={handleEditProfile}>
                    <div className="profile-field">
                        <label className="profile-field-label" htmlFor="display_name">Name</label>
                        <input
                            id="display_name"
                            className="profile-input"
                            type="text"
                            maxLength={150}
                            value={form.display_name}
                            placeholder="Your name"
                            onChange={(e) => setForm({ ...form, display_name: e.target.value })}
                        />
                    </div>

                    <div className="profile-field">
                        <label className="profile-field-label" htmlFor="bio">About me</label>
                        <textarea
                            id="bio"
                            className="profile-input profile-textarea"
                            rows={5}
                            value={form.bio}
                            placeholder="Write something about you"
                            onChange={(e) => setForm({ ...form, bio: e.target.value })}
                        />
                    </div>

                    {saveError && <p className="profile-edit-error">{saveError}</p>}

                    <div className="profile-edit-actions">
                        <button type="button" className="btn btn--ghost" onClick={() => setIsEditing(false)} disabled={saving}>
                            Cancel
                        </button>
                        <button type="submit" className="btn btn--primary" disabled={saving}>
                            {saving ? "Saving..." : "Save changes"}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );

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
                            {profile.bio ? (
                                <p className="profile-section-text">{profile.bio}</p>
                            ) : (
                                <p className="profile-section-empty">Nothing here yet.</p>
                            )}
                        </section>
                        <section className="profile-section">
                            <h2 className="profile-section-label">Gear ratio</h2>
                            <p className="profile-section-empty">Nothing here yet.</p>
                        </section>
                        <section className="profile-section">
                            <h2 className="profile-section-label">Socials</h2>
                            <p className="profile-section-empty">Nothing here yet.</p>
                        </section>
                        <section className="profile-actions">
                            {isOwner && (
                                <button className="btn btn--ghost" onClick={openEditProfile}>Edit profile</button>
                            )}
                            <button className="btn btn--ghost">Share profile</button>
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
