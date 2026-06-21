import { Link } from "react-router-dom";
import "./Home.css";

const HomePage = () => {
    return (
        <div className="home">
            <div className="home-left">
                <h1>Build Your Bike</h1>
                <p>Build the vision of your desired bike! We provide part selection, pricing, and compatibility guidance. Build now!</p>
                <Link to="/builds/new" className="start-build-btn">Build</Link>
            </div>
            <div className="home-right">
                <img src="/engine11.png" alt="bike" />
            </div>
        </div>
    );
};

export default HomePage;
