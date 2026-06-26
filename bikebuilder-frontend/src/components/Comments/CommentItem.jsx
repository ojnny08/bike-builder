import { useState } from "react";

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

const UpvoteIcon = () => (
    <svg {...iconProps}><polyline points="18 15 12 9 6 15" /></svg>
);
const EditIcon = () => (
    <svg {...iconProps}><path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" /></svg>
);
const TrashIcon = () => (
    <svg {...iconProps}><polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" /></svg>
);

const CommentItem = ({ comment, isOwner, canVote, onUpdate, onDelete, onUpvote }) => {
    const [editing, setEditing] = useState(false);
    const [draft, setDraft] = useState(comment.comment);
    const [busy, setBusy] = useState(false);

    const author = comment.user;

    const handleSave = async () => {
        const text = draft.trim();
        if (!text || busy) return;
        setBusy(true);
        try {
            await onUpdate(comment.id, text);
            setEditing(false);
        } finally {
            setBusy(false);
        }
    };

    const handleCancel = () => {
        setDraft(comment.comment);
        setEditing(false);
    };

    const handleDelete = () => {
        if (window.confirm("Delete this comment?")) onDelete(comment.id);
    };

    return (
        <li className="comment-item">
            <div className="comment-vote">
                <button
                    className={`comment-upvote${comment.my_vote ? " is-voted" : ""}`}
                    onClick={() => canVote && onUpvote(comment.id)}
                    disabled={!canVote}
                    aria-pressed={comment.my_vote}
                    aria-label={comment.my_vote ? "Remove upvote" : "Upvote comment"}
                >
                    <UpvoteIcon />
                </button>
                <span className="comment-vote-count">{comment.vote_count}</span>
            </div>

            <div className="comment-body">
                <div className="comment-meta">
                    {author.photo_url
                        ? <img src={author.photo_url} alt={author.display_name} className="comment-avatar" />
                        : <div className="comment-avatar-placeholder">{author.display_name?.[0] ?? "?"}</div>}
                    <span className="comment-author">{author.display_name}</span>
                    {comment.role === "poster" && <span className="comment-badge">Builder</span>}
                    <span className="comment-date">{new Date(comment.created_at).toLocaleDateString()}</span>
                </div>

                {editing ? (
                    <div className="comment-edit">
                        <textarea
                            className="comment-input"
                            value={draft}
                            maxLength={1000}
                            rows={3}
                            onChange={(e) => setDraft(e.target.value)}
                            autoFocus
                        />
                        <div className="comment-edit-actions">
                            <button className="comment-btn-ghost" onClick={handleCancel} disabled={busy}>Cancel</button>
                            <button className="comment-submit" onClick={handleSave} disabled={!draft.trim() || busy}>
                                {busy ? "Saving…" : "Save"}
                            </button>
                        </div>
                    </div>
                ) : (
                    <p className="comment-text">{comment.comment}</p>
                )}

                {isOwner && !editing && (
                    <div className="comment-actions">
                        <button className="comment-action" onClick={() => setEditing(true)} aria-label="Edit comment">
                            <EditIcon /> Edit
                        </button>
                        <button className="comment-action comment-action-danger" onClick={handleDelete} aria-label="Delete comment">
                            <TrashIcon /> Delete
                        </button>
                    </div>
                )}
            </div>
        </li>
    );
};

export default CommentItem;
