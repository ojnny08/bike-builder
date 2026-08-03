import { api } from "../api/axios";
import { toRenderableImage } from "../utils/image";

export const fetchComponents = async (currentCategory) => {
    try {
        const res = await api.get("/api/components/", { params: { category: currentCategory } });
        return res.data.results ?? res.data;
    } catch (error) {
        throw new Error("Failed to get components");
    }
};

export const fetchBuilds = async (params = {}) => {
    try {
        const res = await api.get("/api/builds/", { params });
        return res.data;
    } catch (error) {
        throw new Error("Failed to get builds");
    }
};

// Build the query string by hand so array values (e.g. component ids) repeat
// the key — component=12&component=45 — which Django reads with getlist().
// Axios' default array serialization would emit component[]= and miss it.
const toSearchParams = (params) => {
    const search = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value === null || value === undefined || value === "") return;
        if (Array.isArray(value)) {
            value.forEach(v => search.append(key, v));
            return;
        }
        search.set(key, value);
    });
    return search;
};

export const fetchPublicBuilds = async (params = {}) => {
    try {
        const res = await api.get(`/api/builds/public/?${toSearchParams(params)}`);
        return res.data;
    } catch (error) {
        throw new Error("Failed to get public builds");
    }
};

export const fetchFeaturedBuilds = async () => {
    try {
        const res = await api.get("/api/builds/featured/");
        return res.data;
    } catch (error) {
        throw new Error("Failed to get featured builds");
    }
};

export const getSharedBuild = async (token) => {
    try {
        const res = await api.get(`/api/builds/public/${token}/`);
        return res.data;
    } catch (error) {
        throw new Error("Failed to get shared build");
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

export const createBuild = async (payload, idempotencyKey) => {
    try {
        const res = await api.post("/api/builds/", payload, {
            headers: idempotencyKey ? { "Idempotency-Key": idempotencyKey } : {},
        });
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

export const uploadBuildImage = async (id, file) => {
    try {
        const form = new FormData();
        form.append("image", await toRenderableImage(file));
        const res = await api.post(`/api/builds/${id}/upload-image/`, form);
        return res.data.image_url;
    } catch (error) {
        console.error("uploadBuildImage failed:", error);
        throw new Error("Failed to upload image");
    }
};


