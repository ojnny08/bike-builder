import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js"
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js"

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

    const resize = () => {
        const w = canvas.clientWidth
        const h = canvas.clientHeight
        if (!w || !h) return
        renderer.setSize(w, h, false)
        camera.aspect = w / h
        camera.updateProjectionMatrix()
    }
    resize()

    const resizeObserver = new ResizeObserver(resize)
    resizeObserver.observe(canvas)

    const light = new THREE.DirectionalLight(0xffffff, 2)
    light.position.set(2, 3, 4)
    scene.add(light)
    scene.add(new THREE.AmbientLight(0xffffff, 0.6))

    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;

    let disposed = false
    let model = null

    const loader = new GLTFLoader()
    loader.load("/models/pinarello%20f12.glb", (gltf) => {
        if (disposed) return
        model = gltf.scene

        const box = new THREE.Box3().setFromObject(model)
        const size = box.getSize(new THREE.Vector3())
        const center = box.getCenter(new THREE.Vector3())
        const scale = 3 / Math.max(size.x, size.y, size.z)

        model.position.sub(center)
        model.scale.setScalar(scale)
        scene.add(model)
    })

    let frameId
    const renderloop = () => {
        controls.update();
        renderer.render(scene, camera)
        frameId = window.requestAnimationFrame(renderloop)
    }
    renderloop();

    return () => {
        disposed = true
        resizeObserver.disconnect()
        window.cancelAnimationFrame(frameId)
        if (model) scene.remove(model)
        controls.dispose()
        renderer.dispose()
    }
}
