import { mkdtempSync, realpathSync } from "node:fs";
import { isAbsolute, join, relative, resolve, sep } from "node:path";
import { tmpdir } from "node:os";

export function storyFile(root, requestPath) {
  try {
    const base = realpathSync(root);
    const target = realpathSync(resolve(base, "." + requestPath.replace(/^\/__story\//, "/")));
    const path = relative(base, target);
    return path && path !== ".." && !path.startsWith(".." + sep) && !isAbsolute(path) ? target : null;
  } catch {
    return null;
  }
}

export function createFramesDirectory() {
  return mkdtempSync(join(tmpdir(), "unslop-story-frames-"));
}
