import { api } from "../api/axios";

export const fetchCurrentUser = async () => {
    try {
        const res = await api.get("/api/users/me/");
        return res.data;
    } catch (error) {
        throw new Error("Failed to get user");
    }
};

export const fetchCurrentUserProfile = async () => {
    try {
        const res = await api.get("/api/profile/");
        return res.data;
    } catch (error) {
        throw new Error("Profile DNE")
    }
};

export const fetchCurrentPublicProfile = async (pk) => {
    try {
        const res = await api.get(`/api/profile/${pk}/`);
        return res.data;
    } catch (error) {
        throw new Error("Profile DNE")
    }
};
