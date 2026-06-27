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
    const [description, setDescription] = useState(build.description || "");
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
            description,
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
        } catch {
            // image upload failed — fall through and navigate anyway
        } finally {
            setUploading(false);
            emptyBuild();
            navigate("/builds");
        }
    };

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight) || 0), 0);

    if (uploading) return (
        <div className="pcp-upload-step">
            <div className="pcp-spinner" />
            <p className="pcp-upload-title">Saving your build…</p>
            <p className="pcp-upload-sub">Uploading photo, this will only take a moment</p>
        </div>
    );

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
        <div className="bb-wrapper">
            <div className="bb-main">
                {/* Top bar */}
                <header className="bb-topbar">
                    <div className="bb-topbar-left">
                        <span className="bb-build-type">{build.bikeType.name}</span>
                        <input
                            className="bb-name-input"
                            type="text"
                            placeholder="Name your build…"
                            value={name}
                            onChange={e => setName(e.target.value)}
                        />
                        <textarea
                            className="bb-desc-input"
                            placeholder="Describe your build…"
                            value={description}
                            rows={2}
                            onChange={e => setDescription(e.target.value)}
                        />
                    </div>
                    <div className="bb-topbar-right">
                        <button className="bb-btn-ghost" onClick={emptyBuild}>Start Over</button>
                        <button className="bb-btn-primary" onClick={handleSaveBuild} disabled={saving}>
                            {saving ? "Saving…" : "Save Build"}
                        </button>
                    </div>
                </header>

                {/* Component rows */}
                <div className="bb-list">
                    {allCategories.map(category => {
                        const selected = selectedByCategory[category];
                        const locked = isLocked(category);

                        return (
                            <div
                                key={category}
                                className={`bb-row${locked ? ' is-locked' : ''}`}
                                onClick={() => !locked && navigate(`/builds/new/select/${category}`)}
                            >
                                <span className="bb-row-cat">{formatCat(category)}</span>
                                <div className="bb-row-detail">
                                    {selected ? (
                                        <span className="bb-row-name">{selected.name}
                                            <span className="bb-row-brand"> · {selected.brand}</span>
                                        </span>
                                    ) : locked ? (
                                        <span className="bb-row-msg">Select prerequisite first</span>
                                    ) : (
                                        <span className="bb-row-placeholder">Choose {formatCat(category)}</span>
                                    )}
                                </div>
                                <span className="bb-row-price">
                                    {selected?.price ? `$${parseFloat(selected.price).toFixed(2)}` : '—'}
                                </span>
                            </div>
                        );
                    })}

                    {/* Total — below the last row, right side */}
                    <div className="bb-total">
                        <span className="bb-total-weight">{totalWeight > 0 ? `${totalWeight.toFixed(0)} g` : '—'}</span>
                        <span className="bb-total-price">${totalPrice.toFixed(2)}</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Builder;
