import { api } from "../api/axios";

export const fetchCurrentUserProfile = async () => {
    try {
        const res = await api.get("/api/profile/");
        return res.data;
    } catch (error) {
        const detail = error.response ? `${error.response.status} ${JSON.stringify(error.response.data)}` : error.message;
        throw new Error(`GET /api/profile/ failed: ${detail}`, { cause: error });
    }
};

export const updateCurrentUserProfile = async (payload) => {
    try {
        const res = await api.patch("/api/profile/", payload);
        return res.data;
    } catch (error) {
        const detail = error.response ? `${error.response.status} ${JSON.stringify(error.response.data)}` : error.message;
        throw new Error(`PATCH /api/profile/ failed: ${detail}`, { cause: error });
    }
};

export const deleteCurrentUser = async () => {
    try {
        await api.delete("/api/profile/");
    } catch (error) {
        const detail = error.response ? `${error.response.status} ${JSON.stringify(error.response.data)}` : error.message;
        throw new Error(`DELETE /api/profile/ failed: ${detail}`, { cause: error });
    }
};

export const fetchCurrentPublicProfile = async (pk) => {
    try {
        const res = await api.get(`/api/profile/${pk}/`);
        return res.data;
    } catch (error) {
        const detail = error.response ? `${error.response.status} ${JSON.stringify(error.response.data)}` : error.message;
        throw new Error(`GET /api/profile/${pk}/ failed: ${detail}`, { cause: error });
    }
};

