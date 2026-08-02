import { useEffect } from "react";
import { useBuild } from "../../context/BuildContext";
import { fetchBikeTypes } from "../../services/bikeTypeService";
import BikeStageBuilder from "./components/BikeStageBuilder";

const Builds = () => {
    const { build, updateBuild } = useBuild();

    useEffect(() => {
        if (build.bikeType) return;
        fetchBikeTypes()   
            .then((types) => {
                const fixed = types.find((t) => t.slug === "fixed");
                if (fixed) updateBuild({ bikeType: fixed });
            })
            .catch(console.error);
    }, [build.bikeType]);

    if (!build.bikeType) return <p className="loading-text">Loading…</p>;

    return <BikeStageBuilder />;
};

export default Builds;
