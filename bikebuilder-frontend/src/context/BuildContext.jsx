import { createContext, useContext, useState } from "react"

const BuildContext = createContext();

const EMPTY_BUILD = {
    id: null,
    name: "",
    bikeType: null,
    steps: null,
    components: [],
    status: null
};
export const BuildProvider = ({ children }) => {
    const [build, setBuild] = useState(EMPTY_BUILD);

    const emptyBuild = () => setBuild(EMPTY_BUILD);

    const editBuild = ({ build }) => setBuild(build);

    const updateBuild = (patch) => setBuild((prev) => ({ ...prev, ...patch }));

    const addComponent = (component) => {
        setBuild((prev) => ({
            ...prev,
            components: [
                ...prev.components.filter((c) => c.component_type !== component.component_type),
                component,
            ],
        }));
    };

    return (
        <BuildContext.Provider value={{ build, emptyBuild, updateBuild, addComponent, editBuild }}>
            {children}
        </BuildContext.Provider>
    );
};

export const useBuild = () => useContext(BuildContext);