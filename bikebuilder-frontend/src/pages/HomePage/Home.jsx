import { Link } from "react-router-dom";
import "./Home.css";

const stroke = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
};

const features = [
    {
        title: "Part selection",
        desc: "Browse frames, drivetrains, wheels and finishing kit — every part with an image, spec and price.",
        icon: (
            <svg viewBox="0 0 24 24" {...stroke}><path d="M12 2 2 7l10 5 10-5-10-5Z" /><path d="m2 17 10 5 10-5" /><path d="m2 12 10 5 10-5" /></svg>
        ),
    },
    {
        title: "Live pricing",
        desc: "Your total updates the instant you swap a component, so you always know where the build stands.",
        icon: (
            <svg viewBox="0 0 24 24" {...stroke}><line x1="12" y1="2" x2="12" y2="22" /><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" /></svg>
        ),
    },
    {
        title: "Compatibility",
        desc: "We filter out parts that won't fit, so what you pick actually bolts together.",
        icon: (
            <svg viewBox="0 0 24 24" {...stroke}><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z" /><path d="m9 12 2 2 4-4" /></svg>
        ),
    },
];

const steps = [
    { n: "01", title: "Pick a bike type", desc: "Start from road, gravel or mountain and we set the right part categories." },
    { n: "02", title: "Add your components", desc: "Choose each part and watch the build and price come together in real time." },
    { n: "03", title: "Save & share", desc: "Name your build, add a photo and share it with a link or the community." },
];

const HomePage = () => {
    return (
        <div className="home">
            <section className="home-hero">
                <div className="home-hero-text">
                    <span className="home-eyebrow">
                        <span className="home-eyebrow-dot" />
                        Custom bike configurator
                    </span>
                    <h1 className="home-title">
                        Build your dream bike,<br />
                        <span className="home-title-accent">part by part.</span>
                    </h1>
                    <p className="home-lead">
                        Spec out every component with live pricing and compatibility guidance —
                        then save it, share it, and make it real.
                    </p>
                    <div className="home-cta-row">
                        <Link to="/builds/new" className="home-btn home-btn-primary">
                            Start building
                            <svg width="16" height="16" viewBox="0 0 24 24" {...stroke} strokeWidth="2"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
                        </Link>
                        <Link to="/builds" className="home-btn home-btn-ghost">Browse builds</Link>
                    </div>
                    <div className="home-stats">
                        <div className="home-stat">
                            <span className="home-stat-num">3</span>
                            <span className="home-stat-label">Bike types</span>
                        </div>
                        <div className="home-stat-sep" />
                        <div className="home-stat">
                            <span className="home-stat-num">100+</span>
                            <span className="home-stat-label">Components</span>
                        </div>
                        <div className="home-stat-sep" />
                        <div className="home-stat">
                            <span className="home-stat-num">Live</span>
                            <span className="home-stat-label">Pricing</span>
                        </div>
                    </div>
                </div>
                <div className="home-hero-visual">
                    <div className="home-hero-grid" />
                    <img src="/engine11.png" alt="Bicycle component" className="home-hero-img" />
                    <span className="home-hero-tag">Real-time preview</span>
                </div>
            </section>

            <section className="home-section">
                <h2 className="home-section-title">Everything you need to spec a build</h2>
                <div className="home-features">
                    {features.map((f, i) => (
                        <div className="home-feature" key={f.title} style={{ animationDelay: `${i * 70}ms` }}>
                            <span className="home-feature-icon">{f.icon}</span>
                            <h3 className="home-feature-title">{f.title}</h3>
                            <p className="home-feature-desc">{f.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            <section className="home-section">
                <h2 className="home-section-title">From idea to build in three steps</h2>
                <div className="home-steps">
                    {steps.map((s, i) => (
                        <div className="home-step" key={s.n} style={{ animationDelay: `${i * 70}ms` }}>
                            <span className="home-step-num">{s.n}</span>
                            <h3 className="home-step-title">{s.title}</h3>
                            <p className="home-step-desc">{s.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            <section className="home-band">
                <h2 className="home-band-title">Ready to build your bike?</h2>
                <p className="home-band-sub">No checkout, no pressure — just start speccing.</p>
                <Link to="/builds/new" className="home-btn home-btn-invert">
                    Start building
                    <svg width="16" height="16" viewBox="0 0 24 24" {...stroke} strokeWidth="2"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
                </Link>
            </section>
        </div>
    );
};

export default HomePage;
