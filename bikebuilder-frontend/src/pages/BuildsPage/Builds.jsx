import { useBuild } from "../../context/BuildContext";
import BikeTypeSelection from "./components/BikeTypeSelection";
import BikeStageBuilder from "./components/BikeStageBuilder";

const Builds = () => {
    const { build, updateBuild } = useBuild();

    const handleSelectBikeType = (bikeType) => {
        updateBuild({ bikeType });
    };

    return build.bikeType
        ? <BikeStageBuilder />
        : <BikeTypeSelection onSelect={handleSelectBikeType} />;
};

export default Builds;
