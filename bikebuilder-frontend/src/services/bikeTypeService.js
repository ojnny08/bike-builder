import { api } from "../api/axios";

export const fetchBikeTypes = async () => {
    try {
        const res = await api.get("/api/category/bike-types/");
        return res.data
    } catch (err) {
        throw new Error("Failed to get biketypes")
    }
            
}