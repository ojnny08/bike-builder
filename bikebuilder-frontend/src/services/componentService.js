import { api } from "../api/axios";

export const fetchComponentsByCategory = async (category) => {
    try {
        const res = await api.get("/api/components/", { params: { category } });
        return res.data.results;
    } catch (error) {
        throw new Error("Failed to get components");
    }
};

export const fetchCompatibleComponents = async (category, selectedIds = {}) => {
    try {
        const res = await api.get("/api/components/compatible/", {
            params: { category, ...selectedIds },
        });
        return res.data.results;
    } catch (error) {
        throw new Error("Failed to get compatible components");
    }
};
