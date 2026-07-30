import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import BikeCanvas from "../../threejs/3d-bike/BikeCanvas"
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
        title: "Bike Builder",
        desc: "Spec your dream build and watch the total weight and price update in real time.",
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                <circle cx="18.5" cy="17.5" r="3.5" />
                <circle cx="5.5" cy="17.5" r="3.5" />
                <circle cx="15" cy="5" r="1" />
                <path d="M12 17.5V14l-3-3 4-3 2 3h2" />
            </svg>
        ),
        to: "/builds/new",
    },
    {
        title: "Community",
        desc: "Share your builds, ask for advice and see what everyone else is riding.",
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                <circle cx="9" cy="7" r="4" />
                <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                <path d="M16 3.13a4 4 0 0 1 0 7.75" />
            </svg>
        ),
        to: "/builds",
    },
    {
        title: "Components",
        desc: "Browse a large catalog of parts and import anything that's missing.",
        icon: (
            <svg width="24" height="24" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                <polygon points="12 2 2 7 12 12 22 7 12 2" />
                <polyline points="2 17 12 22 22 17" />
                <polyline points="2 12 12 17 22 12" />
            </svg>
        ),
        to: "/components"
    },
];

const HomePage = () => {
    const offerRef = useRef(null);

    useEffect(() => {
        const observer = new IntersectionObserver(
            ([entry]) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("in-view");
                    observer.unobserve(entry.target);
                }
            },
            { threshold: 0.2 }
        );
        if (offerRef.current) observer.observe(offerRef.current);
        return () => observer.disconnect();
    }, []);

    return (
        <div className="home">
            <section className="home-hero">
                <div className="home-hero-text">
                    <h1 className="home-title">
                        Build & Share your Bikes
                    </h1>
                    <div className="home-cta-row">
                        <Link to="/builds/new" className="home-btn home-btn-primary">
                            Start building
                        </Link>
                </div>   
                </div>
                <div className="home-hero-visual">
                    <div className="home-hero-grid" />
                    <BikeCanvas />
                </div>
            </section>

            <section className="home-section" ref={offerRef}>
                <div className="home-section-head">
                    <h2 className="home-section-title">What We Offer</h2>
                </div>
                <div className="home-steps">
                    {features.map((f) => (
                        <Link className="home-step" to={f.to} key={f.title}>
                            <span className="home-step-icon">{f.icon}</span>
                            <div className="home-step-body">
                                <h3 className="home-step-title">{f.title}</h3>
                                <p className="home-step-desc">{f.desc}</p>
                            </div>
                        </Link>
                    ))}
                </div>
            </section>

            <section className="home-band">
                <h2 className="home-band-title">Ready to build your bike?</h2>
                <p className="home-band-sub">No checkout, no pressure — just start speccing.</p>
                <Link to="/builds/new" className="home-btn home-btn-invert">
                    Start building
                </Link>
            </section>
        </div>
    );
};

export default HomePage;
