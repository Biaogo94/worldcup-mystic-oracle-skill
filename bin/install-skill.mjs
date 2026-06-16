#!/usr/bin/env node
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const repoRoot = path.resolve(__dirname, "..");
const sourceSkill = path.join(repoRoot, "skill", "worldcup-mystic-oracle");

function parseArgs(argv) {
  const args = {
    target: "claude",
    yes: false,
    dryRun: false,
    dest: null,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--target") {
      args.target = argv[++i];
    } else if (token === "--dest") {
      args.dest = argv[++i];
    } else if (token === "--yes" || token === "-y") {
      args.yes = true;
    } else if (token === "--dry-run") {
      args.dryRun = true;
    } else if (token === "--help" || token === "-h") {
      args.help = true;
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  return args;
}

function usage() {
  return [
    "Install worldcup-mystic-oracle skill.",
    "",
    "Usage:",
    "  npx worldcup-mystic-oracle-skill",
    "  npx worldcup-mystic-oracle-skill --target all",
    "  npx worldcup-mystic-oracle-skill --target opencode",
    "  npx worldcup-mystic-oracle-skill --dest ~/.claude/skills",
    "",
    "Targets:",
    "  claude    -> ~/.claude/skills/worldcup-mystic-oracle",
    "  opencode  -> ~/.config/opencode/skills/worldcup-mystic-oracle",
    "  codex     -> ~/.codex/skills/worldcup-mystic-oracle",
    "  agents    -> ~/.agents/skills/worldcup-mystic-oracle",
    "  all       -> claude + opencode + codex + agents",
  ].join("\n");
}

function expandHome(input) {
  if (!input) return input;
  if (input === "~") return os.homedir();
  if (input.startsWith("~/") || input.startsWith("~\\")) {
    return path.join(os.homedir(), input.slice(2));
  }
  return input;
}

function targetDirs(target, dest) {
  if (dest) return [path.resolve(expandHome(dest), "worldcup-mystic-oracle")];
  const home = os.homedir();
  const map = {
    claude: path.join(home, ".claude", "skills", "worldcup-mystic-oracle"),
    opencode: path.join(home, ".config", "opencode", "skills", "worldcup-mystic-oracle"),
    codex: path.join(home, ".codex", "skills", "worldcup-mystic-oracle"),
    agents: path.join(home, ".agents", "skills", "worldcup-mystic-oracle"),
  };
  if (target === "all") return Object.values(map);
  if (!map[target]) throw new Error(`Unsupported target: ${target}`);
  return [map[target]];
}

function copyDir(src, dest, dryRun) {
  if (!fs.existsSync(src)) throw new Error(`Missing skill source: ${src}`);
  if (dryRun) {
    console.log(`[dry-run] copy ${src} -> ${dest}`);
    return;
  }
  fs.rmSync(dest, { recursive: true, force: true });
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.cpSync(src, dest, { recursive: true });
}

function main() {
  let args;
  try {
    args = parseArgs(process.argv);
  } catch (error) {
    console.error(error.message);
    console.error(usage());
    process.exit(2);
  }
  if (args.help) {
    console.log(usage());
    return;
  }

  const dirs = targetDirs(args.target, args.dest);
  for (const dest of dirs) {
    copyDir(sourceSkill, dest, args.dryRun);
    console.log(`${args.dryRun ? "Would install" : "Installed"} worldcup-mystic-oracle -> ${dest}`);
  }
  console.log("");
  console.log("Try in Claude Code/OpenCode:");
  console.log("  使用 worldcup-mystic-oracle，预测 伊拉克 vs 挪威，并给出中国体彩策略。");
}

main();
