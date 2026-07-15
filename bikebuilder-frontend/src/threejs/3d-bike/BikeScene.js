import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"
import { createFrame } from "./frame"

export function createScene(canvas) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(
        50,
        canvas.clientWidth / canvas.clientHeight,
        0.1,
        200,
    )
    camera.position.z = 5

    const renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true })
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
    renderer.setSize(canvas.clientWidth, canvas.clientHeight)

    const frame = createFrame()
    scene.add(frame)

    const light = new THREE.DirectionalLight(0xffffff, 2)
    light.position.set(2, 3, 4)
    scene.add(light)
    scene.add(new THREE.AmbientLight(0xffffff, 0.6))

    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;

    let frameId
    const renderloop = () => {
        controls.update();
        renderer.render(scene, camera)
        frameId = window.requestAnimationFrame(renderloop)
    }
    renderloop();

    window.addEventListener("resize", () => {
        camera.aspect = canvas.clientWidth / canvas.clientHeight
        camera.updateProjectionMatrix()
        renderer.setSize(canvas.clientWidth, canvas.clientHeight)
    })
    return () => {
        window.cancelAnimationFrame(frameId)
        controls.dispose()
        renderer.dispose()
    } 
}
