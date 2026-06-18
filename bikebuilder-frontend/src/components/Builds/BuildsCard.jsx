import { useNavigate } from "react-router-dom";

const BuildsCard = ({ build, onDelete, onEdit }) => {
    const navigate = useNavigate();

    return (
        <div className="build-card">
            <div className="build-card-header">
                <span className="build-bike-type">{build.name}</span>
                <span className={`build-status ${build.status}`}>{build.status.replace("_", " ")}</span>
            </div>
            <p className="build-component-count">{build.components.length} components</p>
            <p className="build-date">{new Date(build.created_at).toLocaleDateString()}</p>
            <button onClick={() => navigate(`/profile/${build.user}`)}>View Profile</button>
            <button className="delete-btn" onClick={() => onDelete(build.id)}>Delete</button>
            <button className="delete-btn" onClick={() => onEdit(build.id)}>Edit</button>
        </div>
    );
};

export default BuildsCard;
