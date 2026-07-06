import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import FilterBar from "../../components/Filters/FilterBar";
import BuildFilters from "../../components/Filters/BuildFilters";
import "./style/PublicBuilds.css";

const PublicBuilds = () => {
    const [buildsList, setBuildsList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [componentIds, setComponentIds] = useState([]);

    // Debounced so typing in the search box doesn't fire a request per keystroke.
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchPublicBuilds({ status: 'complete', search, component: componentIds })
                .then(data => setBuildsList(data))
                .finally(() => setLoading(false));
        }, 300);
        return () => clearTimeout(timer);
    }, [search, componentIds]);

    // Keep the same array reference when the ids haven't actually changed, so
    // the empty first render of BuildFilters doesn't trigger a second fetch.
    const handleFilterChange = useCallback((ids) => {
        setComponentIds(prev => (prev.join(",") === ids.join(",") ? prev : ids));
    }, []);

    const filters = { search, setSearch, activeCount: componentIds.length };

    return (
        <div className="public-builds-page">
            <div className="public-builds-header">
                <div>
                    <h2 className="public-builds-title">Completed Builds</h2>
                </div>
            </div>

            

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
