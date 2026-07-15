import { useEffect, useRef } from "react";
import { createScene } from "./BikeScene";

const BikeCanvas = () => {
    const canvasRef = useRef(null);

    useEffect(() => {
        const cleanup = createScene(canvasRef.current);
        return cleanup;
    }, []);

    return <canvas ref={canvasRef} style={{ width: "100%", height: "100%", display: "block" }} />;
};

export default BikeCanvas;
