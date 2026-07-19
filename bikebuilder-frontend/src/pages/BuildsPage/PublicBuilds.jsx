import { useCallback, useEffect, useRef, useState } from "react";
import { fetchFeaturedBuilds, fetchPublicBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";
import FilterBar from "../../components/Filters/FilterBar";
import BuildFilters from "../../components/Filters/BuildFilters";
import "./style/PublicBuilds.css";

const PublicBuilds = () => {
    const [buildsList, setBuildsList] = useState([]);
    const [loading, setLoading] = useState(true);
    const [search, setSearch] = useState("");
    const [featuredBuilds, setFeaturedBuilds] = useState([]);
    const [componentIds, setComponentIds] = useState([]);
    const featuresRef = useRef(null);

    // Featured builds don't depend on the search/filter state, so fetch once.
    useEffect(() => {
        fetchFeaturedBuilds().then(data => setFeaturedBuilds(data));
    }, []);

    // Debounced so typing in the search box doesn't fire a request per keystroke.
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchPublicBuilds({ status: 'complete', search, component: componentIds })
                .then(data => setBuildsList(data))
                .finally(() => setLoading(false));
        }, 300);
        return () => clearTimeout(timer);
    }, [search, componentIds]);

    // Reveal the featured builds on scroll. JS-only: arm the hidden state
    // (`reveal-ready`) so non-JS / headless renders keep the cards visible,
    // then play the slide-in once the row enters the viewport.
    useEffect(() => {
        const el = featuresRef.current;
        if (!el) return;
        el.classList.add("reveal-ready");
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (!entry.isIntersecting) return;
                el.classList.add("is-visible");
                observer.disconnect();
            },
            { threshold: 0.2 }
        );
        observer.observe(el);
        return () => observer.disconnect();
    }, [featuredBuilds]);

    // Keep the same array reference when the ids haven't actually changed, so
    // the empty first render of BuildFilters doesn't trigger a second fetch.
    const handleFilterChange = useCallback((ids) => {
        setComponentIds(prev => (prev.join(",") === ids.join(",") ? prev : ids));
    }, []);

    const filters = { search, setSearch, activeCount: componentIds.length };

    return (
        <div className="page public-builds-page">

            {featuredBuilds.length > 0 && (
                <section className="featured-builds-section">
                    <h2 className="featured-builds-title">Top Builds This Week</h2>
                    <div className="featured-builds" ref={featuresRef}>
                        {featuredBuilds.map((f, i) => (
                            <div key={f.id} style={{ animationDelay: `${i * 600}ms` }}>
                                <BuildsCard build={f} />
                            </div>
                        ))}
                    </div>
                </section>
            )}

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
