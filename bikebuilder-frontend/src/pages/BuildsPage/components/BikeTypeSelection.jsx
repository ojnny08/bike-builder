import { useEffect, useState } from "react";
import { fetchBikeTypes } from "../../../services/bikeTypeService";

const ACCENT = "#5645d4";

const SLUG_ORDER = ["fixed", "road-gravel", "mountain"];

const IMG_LEFT = {
  "fixed":       "190px",
  "road-gravel": "-134px",
  "mountain":    "-447px",
};

const BikeTypeCard = ({ bikeType, isSelected, onSelect }) => {
  const imgLeft = IMG_LEFT[bikeType.slug] ?? "0px";

  return (
    <div
      role="button"
      tabIndex={0}
      onClick={() => onSelect(bikeType)}
      onKeyDown={(e) => e.key === "Enter" && onSelect(bikeType)}
      style={{
        position: "relative",
        flex: 1,
        height: "calc(100vh - 250px)",
        background: "linear-gradient(160deg, var(--surface, #edecea) 0%, var(--surface-hover, #e5e3df) 100%)",
        border: "1px solid var(--border, #d9d7d2)",
        cursor: "pointer",
        overflow: "hidden",
        boxShadow: isSelected ? "0 16px 34px rgba(40,46,70,.30)" : "0 4px 14px rgba(40,46,70,.12)",
        outline: isSelected ? `4px solid ${ACCENT}` : "4px solid rgba(86,69,212,0)",
        outlineOffset: "-4px",
        transition: "box-shadow .18s ease, outline-color .18s ease",
      }}
    >
      <img
        src="/engine11.png"
        alt=""
        draggable={false}
        style={{
          position: "absolute",
          left: imgLeft,
          top: "200px",
          width: "800px",
          height: "auto",
          pointerEvents: "none",
          userSelect: "none",
        }}
      />

      <div
        style={{
          position: "absolute",
          left: "20px",
          top: "20px",
          fontSize: "0.875rem",
          fontWeight: 600,
          fontFamily: "'Inter', -apple-system, sans-serif",
          color: "var(--text, #1a1a1a)",
          letterSpacing: "-0.02em",
        }}
      >
        {bikeType.name}
      </div>

      {isSelected && (
        <div
          style={{
            position: "absolute",
            left: "20px",
            bottom: "20px",
            display: "flex",
            alignItems: "center",
            gap: "6px",
            color: "var(--text, #1a1a1a)",
            fontWeight: 600,
            fontFamily: "'Inter', -apple-system, sans-serif",
            fontSize: "0.75rem",
            letterSpacing: "-0.01em",
          }}
        >
          <span
            style={{
              display: "inline-block",
              width: "7px",
              height: "7px",
              borderRadius: "50%",
              background: "var(--text, #1a1a1a)",
            }}
          />
          Selected
        </div>
      )}
    </div>
  );
};

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
    <div
      style={{
        margin: "-32px -64px",
        fontFamily: "'Inter', -apple-system, system-ui, sans-serif",
        background: "var(--bg, #f7f6f3)",
        minHeight: "calc(100vh - 110px)",
        boxSizing: "border-box",
      }}
    >
      <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "32px 64px 24px" }}>
        <h2
          style={{
            fontSize: "1.5rem",
            fontWeight: 600,
            color: "var(--text, #1a1a1a)",
            letterSpacing: "-0.03em",
            margin: 0,
          }}
        >
          Choose Your Niche
        </h2>
      </div>

      <div style={{ maxWidth: "1100px", margin: "0 auto", padding: "0 64px" }}>
        {loading ? (
          <p style={{ color: "var(--text-muted, #a4a097)", fontSize: "0.875rem" }}>Loading…</p>
        ) : (
          <div style={{ display: "flex", gap: "16px" }}>
            {[...bikeTypes].sort((a, b) => SLUG_ORDER.indexOf(a.slug) - SLUG_ORDER.indexOf(b.slug)).map((bt) => (
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
