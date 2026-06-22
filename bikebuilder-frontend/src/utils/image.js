import { heicTo, isHeic } from "heic-to";

// Browsers other than Safari can't decode HEIC/HEIF, so convert to JPEG before upload.
// isHeic checks the file's binary signature (not just the extension/MIME), so it
// reliably catches HEICs that iOS reports with an empty or wrong type.
export const toRenderableImage = async (file) => {
    if (!(await isHeic(file))) return file;
    const blob = await heicTo({ blob: file, type: "image/jpeg", quality: 0.9 });
    const name = file.name.replace(/\.hei[cf]$/i, ".jpg");
    return new File([blob], name, { type: "image/jpeg" });
};
