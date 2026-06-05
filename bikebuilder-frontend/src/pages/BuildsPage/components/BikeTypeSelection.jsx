import { useEffect, useState } from "react";
import { api } from "../../../api/axios";
import "../Builds.css";

const DESCRIPTIONS = {
    road: "Built for speed on paved surfaces. Lightweight frames, drop handlebars, and narrow tires optimised for long-distance rides and racing.",
    mountain: "Designed for off-road trails. Durable frames with suspension, wide knobby tires, and flat bars for technical terrain and rough conditions.",
    gravel: "The do-it-all bike. Versatile geometry handles both tarmac and unpaved paths, with wider tire clearance and a more relaxed riding position.",
    fixed: "Pure and simple. A single fixed gear with no freewheel — no derailleur, minimal components, and direct connection between rider and road.",
};

const BikeTypeSelection = ({ onSelect }) => {
    const [bikeTypes, setBikeTypes] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        api.get("/api/category/bike-types/")
            .then(res => setBikeTypes(res.data))
            .finally(() => setLoading(false));
    }, []);

    return (
        <div className="builds-page">
            <h2 className="builds-title">Choose Your Bike Type</h2>
            <p className="builds-subtitle">Select a frame category to start building your ride.</p>
            {loading ? (
                <p className="loading-text">Loading...</p>
            ) : (
                <div className="bike-type-grid">
                    {bikeTypes.map(bt => (
                        <button
                            key={bt.id}
                            className="bike-type-card"
                            onClick={() => onSelect(bt)}
                        >
                            <span className="bike-type-name">{bt.name}</span>
                            <span className="bike-type-desc">{DESCRIPTIONS[bt.slug] ?? ""}</span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default BikeTypeSelection;
