import { createContext, useContext, useState } from "react"

const BuildContext = createContext();

const EMPTY_BUILD = {
    id: null,
    name: "",
    description: "",
    bikeType: null,
    steps: null,
    components: [],
    skipped: [],
    unknown: [],
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
            skipped: (prev.skipped ?? []).filter((t) => t !== component.component_type),
            unknown: (prev.unknown ?? []).filter((t) => t !== component.component_type),
        }));
    };

    const markCategory = (type, kind) => {
        setBuild((prev) => {
            const skipped = (prev.skipped ?? []).filter((t) => t !== type);
            const unknown = (prev.unknown ?? []).filter((t) => t !== type);
            const lists = { skipped, unknown };
            return {
                ...prev,
                components: prev.components.filter((c) => c.component_type !== type),
                ...lists,
                [kind]: [...lists[kind], type],
            };
        });
    };

    return (
        <BuildContext.Provider value={{ build, emptyBuild, updateBuild, addComponent, markCategory, editBuild }}>
            {children}
        </BuildContext.Provider>
    );
};

export const useBuild = () => useContext(BuildContext);