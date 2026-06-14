import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import { fetchComponentsByCategory, fetchCompatibleComponents } from "../../../services/componentService";
import "../Builds.css";

const ComponentSelectPage = () => {
    const { category } = useParams();
    const { build, addComponent } = useBuild();
    const navigate = useNavigate();
    const [components, setComponents] = useState([]);
    const [loading, setLoading] = useState(true);

    const { required = [], optional = [] } = build.bikeType?.rules ?? {};
    const allCategories = [...required, ...optional];

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    useEffect(() => {
        const load = async () => {
            try {
                const selectedIds = Object.fromEntries(
                    allCategories
                        .slice(0, allCategories.indexOf(category))
                        .filter(t => selectedByCategory[t])
                        .map(t => [`${t}_id`, selectedByCategory[t].id])
                );
                const [all, compatible] = await Promise.all([
                    fetchComponentsByCategory(category),
                    category === 'frame'
                        ? Promise.resolve(null)
                        : fetchCompatibleComponents(category, selectedIds),
                ]);
                const compatibleIds = new Set((compatible ?? all).map(c => c.id));
                setComponents(all.map(c => ({ ...c, compatible: compatibleIds.has(c.id) })));
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [category]);

    const handleSelect = (comp) => {
        addComponent(comp);
        navigate("/builds/new");
    };

    return (
        <div className="pcp-wrapper">
            <div className="pcp-main">
                <div className="pcp-topbar">
                    <button className="pcp-start-over" onClick={() => navigate("/builds/new")}>← Back</button>
                </div>
                {loading ? (
                    <p className="loading-text">Loading...</p>
                ) : components.length === 0 ? (
                    <p className="empty-state">No components found.</p>
                ) : (
                    <div className="pcp-picker">
                        {components.map(comp => (
                            <div
                                key={comp.id}
                                className={`pcp-option${!comp.compatible ? ' pcp-option-incompat' : ''}`}
                                onClick={() => comp.compatible && handleSelect(comp)}
                            >
                                <div className="pcp-option-info">
                                    <span className="pcp-option-name">{comp.name}</span>
                                    <span className="pcp-option-brand">{comp.brand}</span>
                                </div>
                                <span className="pcp-option-price">
                                    {comp.price ? `$${parseFloat(comp.price).toFixed(2)}` : '—'}
                                </span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default ComponentSelectPage;
