import { useState, useEffect } from "react";
import { fetchBrands, fetchComponentTypes } from "../services/componentService";

// Shared filter state for component listings: search, type, brand, price range.
// Pass `fixedType` when the category is locked (e.g. picking a part for a build)
// so the type filter is hidden and brands load for that one category.
// `query` is a debounced snapshot the caller feeds into its own fetch effect.
export const useComponentFilters = ({ fixedType = "" } = {}) => {
    const typeLocked = fixedType !== "";

    const [type, setType] = useState(fixedType);
    const [brand, setBrand] = useState("");
    const [search, setSearch] = useState("");
    const [priceMin, setPriceMin] = useState("");
    const [priceMax, setPriceMax] = useState("");
    const [weightMin, setWeightMin] = useState("");
    const [weightMax, setWeightMax] = useState("");

    const [componentTypes, setComponentTypes] = useState([]);
    const [brands, setBrands] = useState([]);
    const [query, setQuery] = useState({ type: fixedType, search: "", brand: "", priceMin: "", priceMax: "", weightMax: "", weightMin: "" });

    // When the locked category changes (navigating between parts), follow it and
    // drop the brand, since the brand list is category-specific.
    useEffect(() => {
        setType(fixedType);
        setBrand("");
    }, [fixedType]);

    // Only load the type list when the user can actually pick a type.
    useEffect(() => {
        if (typeLocked) return;
        fetchComponentTypes()
            .then(setComponentTypes)
            .catch(err => console.log(err));
    }, [typeLocked]);

    useEffect(() => {
        fetchBrands(type)
            .then(setBrands)
            .catch(err => console.log(err));
    }, [type]);

    // Debounce so typing in search/price doesn't fire a request per keystroke.
    useEffect(() => {
        const timer = setTimeout(() => {
            setQuery({ type, search, brand, priceMin, priceMax, weightMax, weightMin });
        }, 300);
        return () => clearTimeout(timer);
    }, [type, search, brand, priceMin, priceMax, weightMax, weightMin]);

    const selectType = (nextType) => {
        setType(nextType);
        setBrand("");
    };

    const clearFilters = () => {
        setType(fixedType);
        setBrand("");
        setSearch("");
        setPriceMin("");
        setPriceMax("");
    };

    const hasFilters = Boolean(brand || search || priceMin || priceMax || weightMax || weightMin || (!typeLocked && type));
    const activeCount = [!typeLocked && type, brand, priceMin || priceMax].filter(Boolean).length;

    return {
        type, brand, search, priceMin, priceMax, weightMax, weightMin,
        setSearch, setBrand, setPriceMin, setPriceMax, setWeightMax, setWeightMin, selectType,
        componentTypes, brands, typeLocked,
        query, hasFilters, activeCount, clearFilters,
    };
};
