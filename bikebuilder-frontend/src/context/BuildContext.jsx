import { createContext, useContext, useState } from "react"

const BuildContext = createContext();

const EMPTY_BUILD = {
    id: null,
    bikeType: null,
    steps: null,
    components: []
};
export const BuildProvider = ({ children }) => {
    const [build, setBuild] = useState(EMPTY_BUILD);

    const startNewBuild = () => setBuild(EMPTY_BUILD);

    const updateBuild = (patch) => setBuild((prev) => ({ ...prev, ...patch }));

    const addComponent = (component) => {
        setBuild((prev) => ({
            ...prev,
            components: [
                ...prev.components.filter((c) => c.category !== component.category),
                component,
            ],
        }));
    };

    return (
        <BuildContext.Provider value={{ build, startNewBuild, updateBuild, addComponent }}>
            {children}
        </BuildContext.Provider>
    );
};

export const useBuild = () => useContext(BuildContext);