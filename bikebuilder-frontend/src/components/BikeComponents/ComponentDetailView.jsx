import { useState, useEffect, useMemo } from "react";
import { fetchComponentDetails } from "../../services/componentService";
import { useBuild } from "../../context/BuildContext";
import VariantOptions from "./VariantOptions";
import ComponentSpecs from "./ComponentSpecs";
import { money } from "../../utils/format";
import "../../pages/Components/ComponentDetails.css";

const ComponentDetailView = ({ id, inBuildFlow, onAdded }) => {
    const { addComponent } = useBuild();
    const [comp, setComp] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(false);
    const [resolved, setResolved] = useState(null);
    const [imgIndex, setImgIndex] = useState(0);

    useEffect(() => {
        setResolved(null);
        setImgIndex(0);
        setLoading(true);
        setError(false);
        fetchComponentDetails(id)
            .then(setComp)
            .catch(() => setError(true))
            .finally(() => setLoading(false));
    }, [id]);

    const images = useMemo(() => {
        if (!comp) return [];
        const all = [comp.image_url, ...(comp.options || []).map(o => o.image_colour_url)];
        return [...new Set(all.filter(Boolean))];
    }, [comp]);

    if (loading) return <p className="loading-text">Loading...</p>;
    if (error || !comp) return <p className="loading-text">Component not found</p>;

    const mainImage = resolved?.image_colour_url || images[imgIndex] || comp.image_url;
    const effectivePrice = Number(resolved?.price) > 0 ? resolved.price : comp.price;

    const addToBuild = () => {
        addComponent({ ...comp, selectedOption: resolved, price: effectivePrice });
        onAdded?.();
    };

    return (
        <div className="comp-view">
            <div className="comp-view-main">
                <div className="comp-view-photo">
                    {mainImage && <img src={mainImage} alt={comp.name} className="comp-view-img" />}
                </div>

                {images.length > 1 && (
                    <div className="comp-view-thumbs">
                        {images.map((src, i) => (
                            <button
                                key={src}
                                type="button"
                                className={`comp-view-thumb${i === imgIndex && !resolved?.image_colour_url ? " is-active" : ""}`}
                                onClick={() => setImgIndex(i)}
                            >
                                <img src={src} alt="" />
                            </button>
                        ))}
                    </div>
                )}
            </div>

            <div className="comp-view-specs">
                <h2 className="comp-view-name">{comp.name}</h2>
                <p className="comp-view-brand">{comp.brand}</p>

                <div className="comp-view-meta">
                    <span className="comp-view-price">{money(effectivePrice)}</span>
                    <span className="comp-view-weight">{comp.weight_grams}g</span>
                </div>

                <VariantOptions options={comp.options} onResolve={setResolved} />

                <h3 className="comp-view-section-title">Specs</h3>
                <ComponentSpecs component={comp} />

                {inBuildFlow && (
                    <button type="button" className="comp-view-add" onClick={addToBuild}>
                        Add to build
                    </button>
                )}

                {comp.import_url && (
                    <a className="comp-view-link" href={comp.import_url} target="_blank" rel="noreferrer">
                        View at retailer
                    </a>
                )}
            </div>
        </div>
    );
};

export default ComponentDetailView;
