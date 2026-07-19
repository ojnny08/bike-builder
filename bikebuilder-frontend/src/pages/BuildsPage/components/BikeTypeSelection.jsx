import { useEffect, useState } from "react";
import { fetchBikeTypes } from "../../../services/bikeTypeService";
import "../style/BikeTypeSelection.css";

const SLUG_ORDER = ["fixed", "road-gravel", "mountain"];

const BikeTypeCard = ({ bikeType, isSelected, onSelect }) => (
  <div
    role="button"
    tabIndex={0}
    className={`bike-type-card${isSelected ? " selected" : ""}`}
    onClick={() => onSelect(bikeType)}
    onKeyDown={(e) => e.key === "Enter" && onSelect(bikeType)}
  >
<div className="bike-type-card-name">{bikeType.name}</div>
    {isSelected && (
      <div className="bike-type-card-selected-badge">
        <span className="bike-type-card-selected-dot" />
        Selected
      </div>
    )}
  </div>
);

const BikeTypeSelection = ({ onSelect }) => {
  const [bikeTypes, setBikeTypes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedId, setSelectedId] = useState(null);

  useEffect(() => {
    fetchBikeTypes()
      .then(setBikeTypes)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  const handleSelect = (bt) => {
    setSelectedId(bt.id);
    onSelect(bt);
  };

  return (
    <div className="page bike-type-selection">
      <div className="bike-type-selection-header">
        <h2 className="bike-type-selection-title">Choose Your Niche</h2>
      </div>
      <div className="bike-type-selection-body">
        {loading ? (
          <p className="loading-text">Loading…</p>
        ) : (
          <div className="bike-type-cards">
            {[...bikeTypes]
              .sort((a, b) => SLUG_ORDER.indexOf(a.slug) - SLUG_ORDER.indexOf(b.slug))
              .map((bt) => (
                <BikeTypeCard
                  key={bt.id}
                  bikeType={bt}
                  isSelected={selectedId === bt.id}
                  onSelect={handleSelect}
                />
              ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default BikeTypeSelection;
