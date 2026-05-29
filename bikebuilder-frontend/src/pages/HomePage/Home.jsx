import { Link } from "react-router-dom";
import hero from "../../assets/hero.png";
import "./Home.css";

const HomePage = () => {
    return (
        <div className="home">
            <div className="home-left">
                <h1>Build Your Bike</h1>
                <p>Choose your components step by step and put together your perfect ride.</p>
                <Link to="/builds" className="start-build-btn">Start Build</Link>
            </div>
            <div className="home-right">
                <img src={hero} alt="bike" />
            </div>
        </div>
    );
};

export default HomePage;
