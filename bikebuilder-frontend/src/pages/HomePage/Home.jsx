import { Link } from "react-router-dom";
import hero from "../../assets/hero.png";
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
                <img src={hero} alt="bike" />
            </div>
        </div>
    );
};

export default HomePage;
