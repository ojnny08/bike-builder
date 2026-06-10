import { api } from "../api/axios";

export const fetchComponentsByCategory = async (category) => {
    try {
        const res = await api.get("/api/components/", { params: { category } });
        return res.data.results ?? res.data;
    } catch (error) {
        throw new Error("Failed to get components");
    }
};
