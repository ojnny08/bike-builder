import { createContext, useContext, useState } from "react"
import AuthPopUp from "../components/Auth/AuthPopUp";

const AuthPopUpContext = createContext();

export const AuthPopUpProvider = ({ children }) => {
    const [isActive, setIsActive] = useState(false);

    return (
        <AuthPopUpContext.Provider value={{ promptLogin: () => setIsActive(true) }}>
            {children}
            {isActive && <AuthPopUp onSelect={() => setIsActive(false)}/>}
        </AuthPopUpContext.Provider>
    )
}
export const useAuthPopUp = () => useContext(AuthPopUpContext);