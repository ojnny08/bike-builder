import { useBuild } from "../../context/BuildContext";

const Builds = () => {
    const { build, startNewBuid, updateBuild} = useBuild();
    

    return (
        <div> builds </div>
    )
}

export default Builds;