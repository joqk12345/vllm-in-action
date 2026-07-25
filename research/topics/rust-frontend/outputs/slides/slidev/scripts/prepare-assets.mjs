import { copyFile, mkdir } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const sourceDir = path.resolve(root, "../../figures");
const targetDir = path.join(root, "public", "figures");
const figures = [
  "rust-frontend-request-lifecycle.svg",
  "rust-workspace-layering.svg",
  "rust-frontend-feature-parity-matrix.svg",
];

await mkdir(targetDir, { recursive: true });
await Promise.all(
  figures.map((name) =>
    copyFile(path.join(sourceDir, name), path.join(targetDir, name)),
  ),
);

console.log(`Synced ${figures.length} shared figures into public/figures.`);
