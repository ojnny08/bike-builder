import { api } from "../api/axios";

export const fetchComments = async (buildId) => {
    try {
        const res = await api.get("/api/comments/", { params: { build: buildId } });
        return res.data;
    } catch (error) {
        throw new Error("Failed to get comments");
    }
};

export const createComment = async (buildId, comment) => {
    try {
        const res = await api.post("/api/comments/", { build: buildId, comment });
        return res.data;
    } catch (error) {
        throw new Error("Failed to create comment");
    }
};

export const updateComment = async (id, comment) => {
    try {
        const res = await api.patch(`/api/comments/${id}/`, { comment });
        return res.data;
    } catch (error) {
        throw new Error("Failed to update comment");
    }
};

export const deleteComment = async (id) => {
    try {
        await api.delete(`/api/comments/${id}/`);
    } catch (error) {
        throw new Error("Failed to delete comment");
    }
};
