import { api } from "../api/axios";

export const fetchCurrentUser = async () => {
    try {
        const res = await api.get("/api/users/me/");
        return res.data;
    } catch (error) {
        throw new Error("Failed to get user");
    }
};
