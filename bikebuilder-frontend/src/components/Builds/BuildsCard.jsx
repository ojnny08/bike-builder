import { useNavigate } from "react-router-dom";

const BuildsCard = ({ build, onDelete, onEdit }) => {
    const navigate = useNavigate();

    return (
        <div className="build-card">
            <div className="build-card-user" onClick={() => navigate(`/profile/${build.user.id}`)}>
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
            {onDelete && <button className="delete-btn" onClick={() => onDelete(build.id)}>Delete</button>}
            {onEdit && <button className="delete-btn" onClick={() => onEdit(build.id)}>Edit</button>}
        </div>
    );
};

export default BuildsCard;
