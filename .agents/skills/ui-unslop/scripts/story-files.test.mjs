import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { storyFile, createFramesDirectory } from "./story-files.mjs";

test("story files stay within the real story root", (t) => {
  const dir = mkdtempSync(join(tmpdir(), "story-check-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const root = join(dir, "story");
  const sibling = join(dir, "story-secret");
  mkdirSync(root); mkdirSync(sibling);
  writeFileSync(join(root, "index.html"), "ok");
  writeFileSync(join(sibling, "secret.txt"), "secret");
  assert.equal(readFileSync(storyFile(root, "/__story/index.html"), "utf8"), "ok");
  assert.equal(storyFile(root, "/__story/../story-secret/secret.txt"), null);
  try {
    symlinkSync(sibling, join(root, "outside"), "junction");
    assert.equal(storyFile(root, "/__story/outside/secret.txt"), null);
  } catch (error) {
    if (!["EPERM", "EACCES", "ENOTSUP"].includes(error.code)) throw error;
  }
});

test("frame directories are unique and preserve existing story files", (t) => {
  const dir = mkdtempSync(join(tmpdir(), "story-owner-"));
  const old = join(dir, ".story-frames");
  mkdirSync(old); writeFileSync(join(old, "keep.txt"), "keep");
  const first = createFramesDirectory(), second = createFramesDirectory();
  t.after(() => { for (const path of [first, second, dir]) rmSync(path, { recursive: true, force: true }); });
  assert.notEqual(first, second);
  assert.equal(readFileSync(join(old, "keep.txt"), "utf8"), "keep");
});
