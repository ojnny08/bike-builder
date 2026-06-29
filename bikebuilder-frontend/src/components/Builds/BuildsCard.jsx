import { useRef, useState } from "react";
import { useNavigate } from "react-router-dom";

const iconProps = {
    width: 15,
    height: 15,
    viewBox: "0 0 24 24",
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 2,
    strokeLinecap: "round",
    strokeLinejoin: "round",
};

const ShareIcon = () => (
    <svg {...iconProps}><circle cx="18" cy="5" r="3" /><circle cx="6" cy="12" r="3" /><circle cx="18" cy="19" r="3" /><line x1="8.6" y1="13.5" x2="15.4" y2="17.5" /><line x1="15.4" y1="6.5" x2="8.6" y2="10.5" /></svg>
);
const CheckIcon = () => (
    <svg {...iconProps}><polyline points="20 6 9 17 4 12" /></svg>
);
const TrashIcon = () => (
    <svg {...iconProps}><polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>
);
const EditIcon = () => (
    <svg {...iconProps}><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></svg>
);
const CameraIcon = () => (
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z" /><circle cx="12" cy="13" r="4" /></svg>
);

const BuildsCard = ({ build, onDelete, onEdit, onUploadImage }) => {
    const navigate = useNavigate();
    const fileInputRef = useRef(null);
    const [copied, setCopied] = useState(false);

    const frame = build.components.find((c) => c.component_type === "frame");
    const crank = build.components.find((c) => c.component_type === "crankset")

    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;
        onUploadImage(build.id, file);
        e.target.value = "";
    };

    const handleShare = async (e) => {
        e.stopPropagation();
        const url = `${window.location.origin}/builds/shared/${build.share_token}`;
        await navigator.clipboard.writeText(url);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div
            className="build-card build-card-clickable"
            onClick={() => navigate(`/builds/view/${build.share_token}`)}
        >
            <div
                className={`build-card-image${onUploadImage ? ' build-card-image-clickable' : ''}`}
                onClick={(e) => { if (onUploadImage) { e.stopPropagation(); fileInputRef.current.click(); } }}
            >
                {build.image_url
                    ? <img src={build.image_url} alt={build.name} className="build-card-img" />
                    : <div className="build-card-img-placeholder">
                        {onUploadImage && <span className="build-card-img-prompt"><CameraIcon /> Add Photo</span>}
                      </div>
                }
                {onUploadImage && build.image_url && (
                    <div className="build-card-img-overlay"><CameraIcon /> Change Photo</div>
                )}
                <button
                    className={`build-card-share${copied ? ' is-copied' : ''}`}
                    onClick={handleShare}
                    aria-label="Share build"
                >
                    {copied ? <CheckIcon /> : <ShareIcon />}
                </button>
            </div>
            {onUploadImage && (
                <input ref={fileInputRef} type="file" accept="image/*" style={{ display: 'none' }} onChange={handleFileChange} />
            )}

            <div className="build-card-user" onClick={(e) => { e.stopPropagation(); navigate(`/profile/${build.user.username}`); }}>
                {build.user.photo_url
                    ? <img src={build.user.photo_url} alt={build.user.display_name} className="build-card-avatar" />
                    : <div className="build-card-avatar-placeholder">{build.user.display_name?.[0] ?? "?"}</div>
                }
                <span className="build-card-username">{build.user.display_name}</span>
            </div>
            <div className="build-card-header">
                <span className="build-bike-type">{build.name}</span>
            </div>
            <div className="build-card-meta">
                <span>{frame ? `${frame.brand} ${frame.name}` : "No frame"}</span>
                <span>{crank ? `${crank.brand} ${crank.name}` : "No crank"}</span>
                <span className="build-card-meta-date">{new Date(build.created_at).toLocaleDateString()}</span>
            </div>
            {(onDelete || onEdit) && (
                <div className="build-card-actions">
                    {onDelete && <button className="icon-btn icon-btn-danger" onClick={(e) => { e.stopPropagation(); onDelete(build.id); }} aria-label="Delete build"><TrashIcon /></button>}
                    {onEdit && <button className="icon-btn" onClick={(e) => { e.stopPropagation(); onEdit(build.id); }} aria-label="Edit build"><EditIcon /></button>}
                </div>
            )}
        </div>
    );
};

export default BuildsCard;
