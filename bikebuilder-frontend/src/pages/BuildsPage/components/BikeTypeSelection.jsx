import { useEffect, useState } from "react";
import { api } from "../../../api/axios";
import "../Builds.css";

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
                            <span className="bike-type-count">
                                {bt.rules?.required?.length ?? 0} components
                            </span>
                        </button>
                    ))}
                </div>
            )}
        </div>
    );
};

export default BikeTypeSelection;
