import * as THREE from "three";

const material = new THREE.MeshStandardMaterial({ color: 0xffffff });

const UP = new THREE.Vector3(0, 1, 0);

const tube = (start, end, radius) => {
    const dir = new THREE.Vector3().subVectors(end, start);
    const length = dir.length();
    const geometry = new THREE.CylinderGeometry(radius, radius, length, 16);
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.copy(start).addScaledVector(dir, 0.5);
    mesh.quaternion.setFromUnitVectors(UP, dir.normalize());
    return mesh;
};

export function createFrame() {
    const v = (x, y) => new THREE.Vector3(x, y, 0);

    const bb = v(0, 0);
    const rearAxle = v(-0.95, 0.05);
    const seatTop = v(-0.2, 0.9);
    const headBottom = v(0.95, 0.45);
    const headTop = v(1.1, 0.8);

    const group = new THREE.Group();
    group.add(
        tube(bb, seatTop, 0.03),
        tube(bb, headBottom, 0.03),
        tube(seatTop, headTop, 0.03),
        tube(headBottom, headTop, 0.04),
        tube(bb, rearAxle, 0.025),
        tube(seatTop, rearAxle, 0.025),
    );

    group.position.set(-0.1, -0.45, 0);
    return group;
}
