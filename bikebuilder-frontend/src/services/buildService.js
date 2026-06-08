import { api } from "../api/axios";

export const fetchComponents = async (currentCategory) => {
    try {
        const res = await api.get("/api/components/componentsList/", { params: { category: currentCategory } });
        return res.data;
    } catch (error) {
        throw new Error("Failed to get components");
    }
};

export const fetchBuilds = async () => {
    try {
        const res = await api.get("/api/builds/");
        return res.data;
    } catch (error) {
        throw new Error("Failed to get builds");
    }
};

export const deleteBuild = async (id) => {
    try {
        const res = await api.delete(`/api/builds/${id}/`);
        return res.data;
    } catch (error) {
        throw new Error("Failed to delete build");
    }
};

export const getBuild = async (id) => {
    try {
        const res = await api.get(`/api/builds/${id}/`);
        return res.data;
    } catch (error) {
        throw new Error("Failed to get build");
    }
};

export const createBuild = async (payload) => {
    try {
        const res = await api.post("/api/builds/", payload);
        return res.data;
    } catch (error) {
        throw new Error("Failed to create build");
    }
};

export const updateBuild = async (id, payload) => {
    try {
        const res = await api.patch(`/api/builds/${id}/`, payload);
        return res.data;
    } catch (error) {
        throw new Error("Failed to update build");
    }
};
