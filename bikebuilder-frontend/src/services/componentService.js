import { api } from "../api/axios";

export const fetchComponentsByCategory = async (category, search = "", brand = "", priceMin = "", priceMax = "") => {
    const res = await api.get("/api/components/", {
        params: { component_type: category, search, brand, price_min: priceMin, price_max: priceMax },
    });
    return res.data.results;
};

export const fetchComponentTypes = async () => {
    const res = await api.get("/api/components/types/");
    return res.data;
};

export const fetchBrands = async (category) => {
    const res = await api.get("/api/components/brands/", {
        params: { component_type: category },
    });
    return res.data;
};

export const fetchCompatibleComponents = async (category, selectedIds = {}) => {
    const res = await api.get("/api/components/compatible/", {
        params: { component_type: category, ...selectedIds },
    });
    return res.data;
};

export const submitProductURL = async (link) => {
    const res = await api.post("/api/components/import_url/", { url: link });
    return res.data;
};