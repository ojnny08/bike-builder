import { useState, useRef } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../../context/BuildContext";
import "../style/Builds.css";
import { createBuild, updateBuild, uploadBuildImage } from "../../../services/buildService";


const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

const Builder = () => {
    const { build, emptyBuild } = useBuild();
    const { required = [], optional = [], prerequisites = {} } = build.bikeType.rules;
    const allCategories = [...required, ...optional];
    const [name, setName] = useState(build.name || "");
    const [saving, setSaving] = useState(false);
    const [savedBuildId, setSavedBuildId] = useState(null);
    const [shareToken, setShareToken] = useState(null);
    const [copied, setCopied] = useState(false);
    const [uploading, setUploading] = useState(false);
    const fileInputRef = useRef(null);
    const navigate = useNavigate();

    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );

    const isLocked = (category) => {
        const dep = prerequisites[category];
        return dep && allCategories.includes(dep) && !selectedByCategory[dep];
    };

    const handleSaveBuild = async () => {
        setSaving(true);
        const selectedTypes = new Set(build.components.map(c => c.component_type));
        const allRequiredFilled = required.every(t => selectedTypes.has(t));
        const payload = {
            name: name || `${build.bikeType.name} Build`,
            bikeType: build.bikeType.id,
            components: build.components.map(c => c.id),
            status: allRequiredFilled ? "complete" : "in_progress",
        };
        try {
            if (build.id) {
                await updateBuild(build.id, payload);
                emptyBuild();
                navigate("/builds");
            } else {
                const saved = await createBuild(payload);
                setSavedBuildId(saved.id);
                setShareToken(saved.share_token);
            }
        } finally {
            setSaving(false);
        }
    };

    const handleCopyShareLink = async () => {
        const url = `${window.location.origin}/builds/shared/${shareToken}`;
        await navigator.clipboard.writeText(url);
        setCopied(true);
    };

    const handleUploadImage = async (file) => {
        setUploading(true);
        try {
            await uploadBuildImage(savedBuildId, file);
        } finally {
            setUploading(false);
            emptyBuild();
            navigate("/builds");
        }
    };

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight) || 0), 0);

    if (savedBuildId) return (
        <div className="pcp-upload-step">
            <p className="pcp-upload-title">Build saved!</p>
            {shareToken && (
                <button className="pcp-start-over" onClick={handleCopyShareLink}>
                    {copied ? "Link copied!" : "Copy share link"}
                </button>
            )}
            <p className="pcp-upload-sub">Add a photo of your bike</p>
            <input
                ref={fileInputRef}
                type="file"
                accept="image/*"
                style={{ display: 'none' }}
                onChange={e => {
                    const file = e.target.files[0];
                    if (file) handleUploadImage(file);
                }}
            />
            <button className="pcp-save-btn" onClick={() => fileInputRef.current.click()} disabled={uploading}>
                {uploading ? "Uploading..." : "Choose Photo"}
            </button>
            <button className="pcp-start-over" onClick={() => { emptyBuild(); navigate("/builds"); }}>
                Skip
            </button>
        </div>
    );

    return (
        <div className="pcp-wrapper">
            <div className="pcp-main">
                {/* Top bar */}
                <div className="pcp-topbar">
                    <div className="pcp-topbar-left">
                        <span className="pcp-build-type">{build.bikeType.name}</span>
                        <input
                            className="pcp-name-input"
                            type="text"
                            placeholder="Name your build..."
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                    </div>
                    <div className="pcp-topbar-right">
                        <button className="pcp-start-over" onClick={emptyBuild}>Start Over</button>
                        <button className="pcp-save-btn" onClick={handleSaveBuild} disabled={saving}>
                            {saving ? "Saving..." : "Save Build"}
                        </button>
                    </div>
                </div>

                {/* Component rows */}
                <div className="pcp-list">
                    {allCategories.map(category => {
                        const selected = selectedByCategory[category];
                        const locked = isLocked(category);

                        return (
                            <div
                                key={category}
                                className={`pcp-item${locked ? ' pcp-item-locked' : ''}`}
                                onClick={() => !locked && navigate(`/builds/new/select/${category}`)}
                            >
                                <span className="pcp-item-cat">{formatCat(category)}</span>
                                <div className="pcp-item-center">
                                    {selected ? (
                                        <span className="pcp-item-selected">{selected.name}
                                            <span className="pcp-item-brand"> · {selected.brand}</span>
                                        </span>
                                    ) : locked ? (
                                        <span className="pcp-item-locked-msg">Select prerequisite first</span>
                                    ) : (
                                        <span className="pcp-item-placeholder">Choose {formatCat(category)}</span>
                                    )}
                                </div>
                                <span className="pcp-item-price">
                                    {selected?.price ? `$${parseFloat(selected.price).toFixed(2)}` : '—'}
                                </span>
                            </div>
                        );
                    })}
                </div>
            </div>

            {/* Summary panel */}
            <div className="pcp-summary">
                <h3 className="pcp-summary-title">Summary</h3>
                <div className="pcp-summary-list">
                    {allCategories.map(category => {
                        const comp = selectedByCategory[category];
                        return (
                            <div key={category} className="pcp-summary-row">
                                <span className="pcp-summary-cat">{formatCat(category)}</span>
                                <span className="pcp-summary-val">
                                    {comp ? comp.name : <span className="pcp-summary-empty">—</span>}
                                </span>
                            </div>
                        );
                    })}
                </div>
                <div className="pcp-summary-totals">
                    {totalWeight > 0 && (
                        <div className="pcp-summary-total-row">
                            <span>Total Weight</span>
                            <span>{totalWeight.toFixed(0)}g</span>
                        </div>
                    )}
                    <div className="pcp-summary-total-row pcp-summary-price">
                        <span>Total Price</span>
                        <span>${totalPrice.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Builder;
