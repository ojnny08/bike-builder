import { useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import BikeCanvas from "../../threejs/3d-bike/BikeCanvas"
import sundayy from "../../utils/sundayy.png";
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
        desc: "Build your bike, get automatic component compatibility, and watch the total weight and price update in real time.",
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
        desc: "Share your bikes, ask for advice, and see what everyone else is riding.",
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
        desc: "Browse our large catalog of parts and import anything components we are missing.",
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

const Home = () => {
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
                    <p className="home-subtitle">show off your bike, view our large component selection, and rate other bikes</p>
                    
                    <div className="home-searchbar">
                        <Link to="/builds/new" className="home-searchbar-seg">Builder</Link>
                        <span className="home-searchbar-divider" aria-hidden="true" />
                        <Link to="/components" className="home-searchbar-seg">Components</Link>
                        <span className="home-searchbar-divider" aria-hidden="true" />
                        <Link to="/builds" className="home-searchbar-seg">Completed bikes</Link>
                        <span className="home-searchbar-search" aria-hidden="true">
                            <svg width="18" height="18" viewBox="0 0 24 24" {...stroke}>
                                <circle cx="11" cy="11" r="7" />
                                <path d="m21 21-4.3-4.3" />
                            </svg>
                        </span>
                    </div>
                </div>
  
                <div className="home-hero-visual">
                    <div className="home-hero-grid" />
                        <BikeCanvas />
                    </div>
            </section>

            
            <section className="home-bikestores">
                <h2 className="home-bikestores-title">Visit Sunday Cyclery</h2>
                <div className="home-bikestores-logos">
                    <img className="home-bikestores-logo" src={sundayy} alt="Sunday" />
                </div>
            </section>

            <section className="home-section" ref={offerRef}>
                <div className="home-section-head">
                    <h2 className="home-section-title">Bikeco Features</h2>
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

            <section className="home-footer">
                <h2 className="home-footer-title">What are you waiting for?</h2>
                <div className="home-footer-links">
                    <Link to="/builds/new" className="home-footer-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                        <path d="M14.7 6.3a4 4 0 0 0-5.4 5.3L3 18l3 3 6.4-6.3a4 4 0 0 0 5.3-5.4l-2.4 2.4-2.6-.7-.7-2.6z" />
                    </svg>
                    Start Building
                </Link>
                <Link to="/components" className="home-footer-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                        <polygon points="12 2 2 7 12 12 22 7 12 2" />
                        <polyline points="2 17 12 22 22 17" />
                        <polyline points="2 12 12 17 22 12" />
                    </svg>
                    Explore Components
                </Link>
                <Link to="/builds" className="home-footer-btn">
                    <svg width="18" height="18" viewBox="0 0 24 24" {...stroke} aria-hidden="true">
                        <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                        <circle cx="9" cy="7" r="4" />
                        <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
                        <path d="M16 3.13a4 4 0 0 1 0 7.75" />
                    </svg>
                    View Completed Bikes
                </Link>
                </div>
            </section>

            <footer className="site-footer">
                <div className="site-footer-inner">
                    <div className="site-footer-brand">
                        <span className="site-footer-logo">Bikeco</span>
                        <p className="site-footer-tag">Build & share your dream bikes.</p>
                    </div>

                    <div className="site-footer-cols">
                        <div className="site-footer-col">
                            <h4 className="site-footer-heading">Company</h4>
                            <Link to="/about">About</Link>
                            <Link to="/blog">Blog</Link>
                            <Link to="/careers">Careers</Link>
                            <Link to="/contact">Contact</Link>
                        </div>

                        <div className="site-footer-col">
                            <h4 className="site-footer-heading">Social</h4>
                            <a href="https://twitter.com" target="_blank" rel="noreferrer">Twitter</a>
                            <a href="https://instagram.com" target="_blank" rel="noreferrer">Instagram</a>
                            <a href="https://youtube.com" target="_blank" rel="noreferrer">YouTube</a>
                            <a href="https://discord.com" target="_blank" rel="noreferrer">Discord</a>
                        </div>

                        <div className="site-footer-col">
                            <h4 className="site-footer-heading">Legal</h4>
                            <Link to="/terms">Terms</Link>
                            <Link to="/privacy">Privacy</Link>
                            <Link to="/cookies">Cookies</Link>
                        </div>
                    </div>
                </div>

                <div className="site-footer-bottom">
                    <span>© 2026 Bikeco. All rights reserved.</span>
                </div>
            </footer>
        </div>
    );
};

export default Home;
