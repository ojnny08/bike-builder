import { useBuild } from "../../context/BuildContext";
import BikeTypeSelection from "./components/BikeTypeSelection";
import Builder from "./components/Builder";

const Builds = () => {
    const { build, updateBuild } = useBuild();

    const handleSelectBikeType = (bikeType) => {
        updateBuild({ bikeType });
    };

    return build.bikeType
        ? <Builder />
        : <BikeTypeSelection onSelect={handleSelectBikeType} />;
};

export default Builds;
