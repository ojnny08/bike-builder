import { api } from "../api/axios";

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

