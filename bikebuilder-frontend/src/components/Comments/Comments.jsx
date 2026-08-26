import { useEffect, useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { fetchCurrentUserProfile } from "../../services/userService";
import {
    fetchComments,
    createComment,
    updateComment,
    deleteComment,
} from "../../services/commentService";
import CommentItem from "./CommentItem";
import "./Comments.css";

const Comments = ({ buildId }) => {
    const { currentUser } = useAuth();
    const [comments, setComments] = useState([]);
    const [loading, setLoading] = useState(true);
    const [myUsername, setMyUsername] = useState(null);
    const [draft, setDraft] = useState("");
    const [posting, setPosting] = useState(false);
    const [showForm, setShowForm] = useState(false);

    useEffect(() => {
        if (!buildId) return;
        fetchComments(buildId)
            .then(setComments)
            .finally(() => setLoading(false));
    }, [buildId]);

    useEffect(() => {
        if (!currentUser) return;
        fetchCurrentUserProfile()
            .then((profile) => setMyUsername(profile.username))
            .catch(() => {});
    }, [currentUser]);

    const handlePost = async (e) => {
        e.preventDefault();
        const text = draft.trim();
        if (!text || posting) return;
        setPosting(true);
        try {
            const created = await createComment(buildId, text);
            setComments((prev) => [created, ...prev]);
            setDraft("");
            setShowForm(false);
        } finally {
            setPosting(false);
        }
    };

    const handleUpdate = async (id, text) => {
        const updated = await updateComment(id, text);
        setComments((prev) => prev.map((c) => (c.id === id ? updated : c)));
    };

    const handleDelete = async (id) => {
        await deleteComment(id);
        setComments((prev) => prev.filter((c) => c.id !== id));
    };


    return (
        <section className="comments">
            <h3 className="comments-title">
                Comments <span className="comments-count">{comments.length}</span>
            </h3>

            {currentUser ? (
                showForm ? (
                    <form className="comment-form" onSubmit={handlePost}>
                        <label htmlFor="comment-input" className="sr-only">Add a comment</label>
                        <textarea
                            id="comment-input"
                            className="comment-input"
                            placeholder="Share your thoughts on this build…"
                            value={draft}
                            maxLength={1000}
                            rows={3}
                            autoFocus
                            onChange={(e) => setDraft(e.target.value)}
                        />
                        <div className="comment-form-footer">
                            <span className="comment-charcount">{draft.length}/1000</span>
                            <div className="comment-form-actions">
                                <button
                                    type="button"
                                    className="btn btn--ghost"
                                    onClick={() => { setShowForm(false); setDraft(""); }}
                                >
                                    Cancel
                                </button>
                                <button type="submit" className="btn btn--primary" disabled={!draft.trim() || posting}>
                                    {posting ? "Posting…" : "Post comment"}
                                </button>
                            </div>
                        </div>
                    </form>
                ) : (
                    <button type="button" className="btn btn--primary mb-7" onClick={() => setShowForm(true)}>
                        Add a comment
                    </button>
                )
            ) : (
                <p className="comments-signed-out">Sign in to join the conversation.</p>
            )}

            {loading ? (
                <p className="comments-loading">Loading comments…</p>
            ) : comments.length === 0 ? (
                <p className="comments-empty">No comments yet. Be the first to share your thoughts.</p>
            ) : (
                <ul className="comment-list">
                    {comments.map((c) => (
                        <CommentItem
                            key={c.id}
                            comment={c}
                            isOwner={!!myUsername && c.user.username === myUsername}
                            onUpdate={handleUpdate}
                            onDelete={handleDelete}
                        />
                    ))}
                </ul>
            )}
        </section>
    );
};

export default Comments;
