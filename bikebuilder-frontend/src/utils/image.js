import { heicTo, isHeic } from "heic-to";

// Downscaling and re-encoding to JPEG keeps uploads small so they reach S3 fast.
// Phone photos are often 4000px+ / several MB; 1600px at 0.8 quality is plenty for display.
const MAX_DIMENSION = 1600;
const JPEG_QUALITY = 0.8;

const compressImage = async (file) => {
    const bitmap = await createImageBitmap(file);
    const scale = Math.min(1, MAX_DIMENSION / Math.max(bitmap.width, bitmap.height));
    const width = Math.round(bitmap.width * scale);
    const height = Math.round(bitmap.height * scale);

    const canvas = document.createElement("canvas");
    canvas.width = width;
    canvas.height = height;
    canvas.getContext("2d").drawImage(bitmap, 0, 0, width, height);
    bitmap.close();

    const blob = await new Promise(resolve => canvas.toBlob(resolve, "image/jpeg", JPEG_QUALITY));
    const name = file.name.replace(/\.[^.]+$/, ".jpg");
    return new File([blob], name, { type: "image/jpeg" });
};

// Browsers other than Safari can't decode HEIC/HEIF, so convert to JPEG before upload.
// isHeic checks the file's binary signature (not just the extension/MIME), so it
// reliably catches HEICs that iOS reports with an empty or wrong type.
export const toRenderableImage = async (file) => {
    // PNGs are kept as-is: re-encoding to JPEG would flatten transparency.
    if (file.type === "image/png") return file;

    let normalized = file;
    const heic = await isHeic(file)

    if (heic) {
        const blob = await heicTo({ blob: file, type: "image/jpeg", quality: 0.9 });
        normalized = new File([blob], file.name.replace(/\.hei[cf]$/i, ".jpg"), { type: "image/jpeg" });
    }
    return compressImage(normalized);
};
