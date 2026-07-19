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
    },
];

const HomePage = () => {
    return (
        <div className="home">
            <section className="home-hero">
                <div className="home-hero-text">
                    <h1 className="home-title">
                        Build & Share your Bike With Others
                    </h1>
                    <div className="home-cta-row">
                        <Link to="/builds/new" className="home-btn home-btn-primary">
                            Start building
                        </Link>
                </div>   
                </div>
                <div className="home-hero-visual">
                    <div className="home-hero-grid" />
                    <img src="/engine11.png" alt="Bicycle component" className="home-hero-img" />
                </div>
            </section>

            <section className="home-section">
                <div className="home-section-head">
                    <h2 className="home-section-title">What We Offer</h2>
                </div>
                <div className="home-steps">
                    {features.map((f, i) => (
                        <div className="home-step" key={f.title} style={{ animationDelay: `${i * 70}ms` }}>
                            <span className="home-step-icon">{f.icon}</span>
                            <div className="home-step-body">
                                <h3 className="home-step-title">{f.title}</h3>
                                <p className="home-step-desc">{f.desc}</p>
                            </div>
                        </div>
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
