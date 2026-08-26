import { useCallback, useEffect, useState } from "react";
import { fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import FilterBar from "../../components/Filters/FilterBar";
import BuildFilters from "../../components/Filters/BuildFilters";
import "../../styles/pages/Builds/PublicBuilds.css";

const PublicBuilds = () => {
    const [buildsList, setBuildsList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [componentIds, setComponentIds] = useState([]);

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchPublicBuilds({ status: 'complete', search, component: componentIds })
                .then(data => setBuildsList(data))
                .finally(() => setLoading(false));
        }, 300);
        return () => clearTimeout(timer);
    }, [search, componentIds]);

    const handleFilterChange = useCallback((ids) => {
        setComponentIds(prev => (prev.join(",") === ids.join(",") ? prev : ids));
    }, []);

    const filters = { search, setSearch, activeCount: componentIds.length };

    return (
        <div className="page public-builds-page">

            <FilterBar
                filters={filters}
                searchPlaceholder="Search builds..."
                iconOnly
                centered
                panel={<BuildFilters onChange={handleFilterChange} />}
            />

            {loading ? (
                <p className="loading-text">Loading...</p>
            ) : buildsList.length === 0 ? (
                <p className="loading-text">No builds match these filters.</p>
            ) : (
                <div className="builds-grid">
                    {buildsList.map((build) => (
                        <BuildsCard
                            key={build.id}
                            build={build}
                        />
                    ))}
                </div>
            )}
        </div>
    );
};

export default PublicBuilds;
