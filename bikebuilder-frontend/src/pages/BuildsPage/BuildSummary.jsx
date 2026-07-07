import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useBuild } from "../../context/BuildContext";
import BuilderNav from "./components/BuilderNav";
import { createBuild, updateBuild as updateBuildApi, uploadBuildImage } from "../../services/buildService";
import "./style/Builds.css";

const formatCat = s => s.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
const money = n => `$${n.toFixed(2)}`;

const PartGlyph = () => (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.4"
        strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
        <circle cx="12" cy="12" r="3.2" />
        <path d="M12 2.6v3M12 18.4v3M2.6 12h3M18.4 12h3M5.4 5.4l2.1 2.1M16.5 16.5l2.1 2.1M18.6 5.4l-2.1 2.1M7.5 16.5l-2.1 2.1" />
    </svg>
);

const Thumb = ({ src }) => (
    <span className="bb-thumb">
        {src ? <img src={src} alt="" loading="lazy" /> : <span className="bb-thumb-glyph"><PartGlyph /></span>}
    </span>
);

const BuildSummary = () => {
    const { build, emptyBuild, updateBuild: patchBuild } = useBuild();
    const navigate = useNavigate();

    const [name, setName] = useState(build.name || "");
    const [description, setDescription] = useState(build.description || "");
    const [photoFile, setPhotoFile] = useState(null);
    const [photoPreview, setPhotoPreview] = useState(null);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState(null);
    const fileInputRef = useRef(null);

    // Reached directly without a bike type in progress — nothing to review.
    useEffect(() => {
        if (!build.bikeType) navigate("/builds/new", { replace: true });
    }, [build.bikeType, navigate]);
    if (!build.bikeType) return null;

    const { required = [] } = build.bikeType.rules;
    const selectedByCategory = Object.fromEntries(
        build.components.map(c => [c.component_type, c])
    );
    const requiredFilled = required.filter(t => selectedByCategory[t]).length;
    const allRequiredFilled = required.length > 0 && requiredFilled === required.length;

    const totalPrice = build.components.reduce((sum, c) => sum + (parseFloat(c.price) || 0), 0);
    const totalWeight = build.components.reduce((sum, c) => sum + (parseFloat(c.weight_grams) || 0), 0);

    const handleName = (v) => { setName(v); patchBuild({ name: v }); };
    const handleDescription = (v) => { setDescription(v); patchBuild({ description: v }); };

    const handlePhoto = (file) => {
        if (!file) return;
        setPhotoFile(file);
        setPhotoPreview(URL.createObjectURL(file));
    };

    const clearPhoto = () => {
        if (photoPreview) URL.revokeObjectURL(photoPreview);
        setPhotoFile(null);
        setPhotoPreview(null);
        if (fileInputRef.current) fileInputRef.current.value = "";
    };

    const handleSave = async () => {
        setSaving(true);
        setError(null);
        const payload = {
            name: name.trim() || `${build.bikeType.name} Build`,
            description: description.trim(),
            bikeType: build.bikeType.id,
            components: build.components.map(c => c.id),
            status: allRequiredFilled ? "complete" : "in_progress",
        };
        try {
            let id = build.id;
            if (id) await updateBuildApi(id, payload);
            else id = (await createBuild(payload)).id;
            if (photoFile) await uploadBuildImage(id, photoFile);
            emptyBuild();
            navigate("/builds");
        } catch (e) {
            console.error(e);
            setError("Something went wrong saving your build. Please try again.");
            setSaving(false);
        }
    };

    return (
        <div className="bb-wrapper">
            <BuilderNav hideSave />
            <div className="sm-main">
                <header className="sm-head">
                    <button className="bb-btn-ghost" onClick={() => navigate("/builds/new")} disabled={saving}>
                        ← Back to parts
                    </button>
                    <h1 className="sm-title">Review &amp; save your build</h1>
                </header>

                <div className="sm-grid">
                    {/* Recap */}
                    <section className="sm-recap" aria-label="Build summary">
                        <div className="sm-recap-head">
                            <span className="sm-recap-type">{build.bikeType.name}</span>
                            <span className={`sm-status${allRequiredFilled ? ' is-complete' : ''}`}>
                                {allRequiredFilled ? 'Complete' : `${requiredFilled}/${required.length} essentials`}
                            </span>
                        </div>
                        <ul className="sm-recap-list">
                            {build.components.length === 0 && (
                                <li className="sm-recap-empty">No components added yet.</li>
                            )}
                            {build.components.map(c => (
                                <li key={c.id} className="sm-recap-row">
                                    <Thumb src={c.image_url} />
                                    <div className="sm-recap-info">
                                        <span className="sm-recap-cat">{formatCat(c.component_type)}</span>
                                        <span className="sm-recap-name">{c.name}<span className="bb-row-brand"> · {c.brand}</span></span>
                                    </div>
                                    <span className="sm-recap-price">{c.price ? money(parseFloat(c.price)) : '—'}</span>
                                </li>
                            ))}
                        </ul>
                        <div className="sm-recap-totals">
                            <span className="sm-recap-weight">{totalWeight > 0 ? `${totalWeight.toFixed(0)} g` : '—'}</span>
                            <span className="sm-recap-total">{money(totalPrice)}</span>
                        </div>
                    </section>

                    {/* Form */}
                    <section className="sm-form" aria-label="Build details">
                        <div className="sm-field">
                            <label className="sm-label" htmlFor="build-name">Build name</label>
                            <input
                                id="build-name"
                                className="sm-input"
                                type="text"
                                placeholder={`${build.bikeType.name} Build`}
                                value={name}
                                onChange={e => handleName(e.target.value)}
                                maxLength={80}
                            />
                        </div>

                        <div className="sm-field">
                            <label className="sm-label" htmlFor="build-desc">Description <span className="sm-optional">optional</span></label>
                            <textarea
                                id="build-desc"
                                className="sm-textarea"
                                placeholder="What's the story behind this build? Intended use, standout parts, fit notes…"
                                value={description}
                                rows={4}
                                onChange={e => handleDescription(e.target.value)}
                            />
                        </div>

                        <div className="sm-field">
                            <span className="sm-label">Photo <span className="sm-optional">optional</span></span>
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/*"
                                style={{ display: 'none' }}
                                onChange={e => handlePhoto(e.target.files[0])}
                            />
                            {photoPreview ? (
                                <div className="sm-photo">
                                    <img src={photoPreview} alt="Build preview" className="sm-photo-img" />
                                    <div className="sm-photo-actions">
                                        <button className="bb-btn-ghost" onClick={() => fileInputRef.current.click()}>Replace</button>
                                        <button className="bb-btn-ghost" onClick={clearPhoto}>Remove</button>
                                    </div>
                                </div>
                            ) : (
                                <button className="sm-dropzone" onClick={() => fileInputRef.current.click()}>
                                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                        strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" />
                                    </svg>
                                    <span className="sm-dropzone-text">Add a photo of your bike</span>
                                    <span className="sm-dropzone-hint">JPG, PNG or HEIC</span>
                                </button>
                            )}
                        </div>

                        {error && <p className="sm-error" role="alert">{error}</p>}

                        <div className="sm-actions">
                            <button className="bb-btn-primary bb-btn-lg" onClick={handleSave} disabled={saving}>
                                {saving ? "Saving…" : "Save build"}
                            </button>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default BuildSummary;
