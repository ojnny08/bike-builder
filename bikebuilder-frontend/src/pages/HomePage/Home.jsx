import { Link } from "react-router-dom";
import "./Home.css";
import { useEffect, useRef, useState } from "react";
import { fetchFeaturedBuilds } from "../../services/buildService";
import BuildsCard from "../../components/Builds/BuildsCard";

const stroke = {
    fill: "none",
    stroke: "currentColor",
    strokeWidth: 1.8,
    strokeLinecap: "round",
    strokeLinejoin: "round",
};


const steps = [
    { n: "01", title: "Pick a bike type", desc: "Start from road, gravel or mountain and we set the right part categories." },
    { n: "02", title: "Add your components", desc: "Choose each part and watch the build and price come together in real time." },
    { n: "03", title: "Save & share", desc: "Name your build, add a photo and share it with a link or the community." },
];

const HomePage = () => {
    const [threeBuilds, setThreeBuilds] = useState([]);
    const featuresRef = useRef(null);

    const handleThreeBuilds = async () => {
        const data = await fetchFeaturedBuilds();
        setThreeBuilds(data);
    }

    useEffect(() => {
        handleThreeBuilds();
    }, [])

    // Reveal the featured builds on scroll. JS-only: arm the hidden state
    // (`reveal-ready`) so non-JS / headless renders keep the cards visible,
    // then play the slide-in once the row enters the viewport.
    useEffect(() => {
        const el = featuresRef.current;
        if (!el) return;
        el.classList.add("reveal-ready");
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (!entry.isIntersecting) return;
                el.classList.add("is-visible");
                observer.disconnect();
            },
            { threshold: 0.2 }
        );
        observer.observe(el);
        return () => observer.disconnect();
    }, [threeBuilds])
    
    return (
        <div className="home">
            <section className="home-hero">
                <div className="home-hero-text">
                    <h1 className="home-title">
                        Build your bike
                    </h1>
                    <div className="home-cta-row">
                        <Link to="/builds/new" className="home-btn home-btn-primary">
                            Start building
                            <svg width="16" height="16" viewBox="0 0 24 24" {...stroke} strokeWidth="2"><line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" /></svg>
                        </Link>
                        
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
                <h2 className="home-section-title">Top Builds This Week</h2>
                <div className="home-features" ref={featuresRef}>
                    {threeBuilds.map((f, i) => (
                        <div key={f.id} style={{ animationDelay: `${i * 600}ms` }}>
                            <BuildsCard build={f} />
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
