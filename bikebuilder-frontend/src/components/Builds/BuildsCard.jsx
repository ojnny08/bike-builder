import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

const BuildsCard = ({ build, onDelete, onEdit, onUploadImage }) => {
    const navigate = useNavigate();
    const fileInputRef = useRef(null);
    const [copied, setCopied] = useState(false);

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        onUploadImage(build.id, file);
        e.target.value = "";
    };

    const handleShare = async () => {
        const url = `${window.location.origin}/builds/shared/${build.share_token}`;
        await navigator.clipboard.writeText(url);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="build-card">
            <div
                className={`build-card-image${onUploadImage ? ' build-card-image-clickable' : ''}`}
                onClick={() => onUploadImage && fileInputRef.current.click()}
            >
                {build.image_url
                    ? <img src={build.image_url} alt={build.name} className="build-card-img" />
                    : <div className="build-card-img-placeholder">
                        {onUploadImage && <span className="build-card-img-prompt">+ Add Photo</span>}
                      </div>
                }
                {onUploadImage && build.image_url && (
                    <div className="build-card-img-overlay">Change Photo</div>
                )}
            </div>
            {onUploadImage && (
                <input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileChange} />
            )}

            <div className="build-card-user" onClick={() => navigate(`/profile/${build.user.username}`)}>
                {build.user.photo_url
                    ? <img src={build.user.photo_url} alt={build.user.display_name} className="build-card-avatar" />
                    : <div className="build-card-avatar-placeholder">{build.user.display_name?.[0] ?? "?"}</div>
                }
                <span className="build-card-username">{build.user.display_name}</span>
            </div>
            <div className="build-card-header">
                <span className="build-bike-type">{build.name}</span>
                <span className={`build-status ${build.status}`}>{build.status.replace("_", " ")}</span>
            </div>
            <p className="build-component-count">{build.components.length} components</p>
            <p className="build-date">{new Date(build.created_at).toLocaleDateString()}</p>
            <button className="share-btn" onClick={handleShare}>{copied ? "Link copied!" : "Share"}</button>
            {onDelete && <button className="delete-btn" onClick={() => onDelete(build.id)}>Delete</button>}
            {onEdit && <button className="delete-btn" onClick={() => onEdit(build.id)}>Edit</button>}
        </div>
    );
};

export default BuildsCard;
