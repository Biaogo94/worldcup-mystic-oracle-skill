#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const PALACE_INFO = {
  "1": { name: "坎", direction: "正北", element: "shui" },
  "2": { name: "坤", direction: "西南", element: "tu" },
  "3": { name: "震", direction: "正东", element: "mu" },
  "4": { name: "巽", direction: "东南", element: "mu" },
  "5": { name: "中", direction: "中宫", element: "tu" },
  "6": { name: "乾", direction: "西北", element: "jin" },
  "7": { name: "兑", direction: "正西", element: "jin" },
  "8": { name: "艮", direction: "东北", element: "tu" },
  "9": { name: "离", direction: "正南", element: "huo" },
};

function parseArgs(argv) {
  const args = {
    method: "时家",
    purpose: "football match prediction",
    location: "",
    pretty: false,
  };
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (token === "--pretty") {
      args.pretty = true;
    } else if (token === "--datetime") {
      args.datetime = argv[++i];
    } else if (token === "--engine-dir") {
      args.engineDir = argv[++i];
    } else if (token === "--method") {
      args.method = argv[++i];
    } else if (token === "--purpose") {
      args.purpose = argv[++i];
    } else if (token === "--location") {
      args.location = argv[++i];
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
    "Usage:",
    "  node scripts/qimen_qfdk.js --engine-dir /path/to/qfdk-qimen --datetime 2026-06-14T12:00:00-05:00 --pretty",
    "",
    "Notes:",
    "  --datetime should include the venue-local UTC offset when possible.",
    "  If --engine-dir is omitted, QIMEN_QFDK_PATH or QIMEN_ENGINE_PATH is used.",
  ].join("\n");
}

function findEngineDir(inputDir) {
  const candidates = [
    inputDir,
    process.env.QIMEN_QFDK_PATH,
    process.env.QIMEN_ENGINE_PATH,
    path.resolve(__dirname, "..", "vendor", "qfdk-qimen"),
  ].filter(Boolean);

  for (const candidate of candidates) {
    const full = path.resolve(candidate);
    if (fs.existsSync(path.join(full, "lib", "qimen.js"))) {
      return full;
    }
  }
  return null;
}

function parseWallDate(input) {
  const match = String(input).match(
    /^(\d{4})-(\d{2})-(\d{2})(?:[T\s](\d{2}):(\d{2})(?::(\d{2}))?)?(?:\.\d+)?(Z|[+-]\d{2}:?\d{2})?$/,
  );
  if (!match) {
    return null;
  }
  const [, year, month, day, hour = "00", minute = "00", second = "00", offset = null] = match;
  return {
    date: new Date(
      Number(year),
      Number(month) - 1,
      Number(day),
      Number(hour),
      Number(minute),
      Number(second),
      0,
    ),
    wallTime: `${year}-${month}-${day}T${hour}:${minute}:${second}`,
    offset,
  };
}

function includesPalace(value, palace) {
  if (Array.isArray(value)) return value.map(String).includes(String(palace));
  if (value && typeof value === "object") return Object.values(value).map(String).includes(String(palace));
  if (value == null) return false;
  return String(value).split(/[,\s，、]+/).includes(String(palace));
}

function normalizePan(pan, args, engineDir, date) {
  const palaces = {};
  for (let i = 1; i <= 9; i += 1) {
    const key = String(i);
    palaces[key] = {
      palace: key,
      ...PALACE_INFO[key],
      di_pan: pan.diPan?.[key],
      tian_pan: pan.tianPan?.[key] ?? pan.sanQiLiuYi?.[key],
      an_gan: pan.anGan?.[key],
      door: pan.baMen?.[key],
      star: pan.jiuXing?.[key],
      deity: pan.baShen?.[key],
      kong_wang: includesPalace(pan.kongWangGong, key),
      analysis: pan.jiuGongAnalysis?.[key],
    };
  }

  return {
    schema: "worldcup-mystic-oracle/qimen-qfdk-v1",
    status: "parsed",
    engine: "qfdk/qimen",
    engine_source: "https://github.com/qfdk/qimen",
    engine_dir: engineDir,
    engine_license_note: "Repository README says MIT; package.json says ISC. Treat as permissive and cite source if bundled.",
    chart_standard: "qfdk/qimen 茅山派奇门遁甲, 转盘排法",
    method: args.method,
    datetime_input: args.datetime,
    datetime_wall_time: args.wallTime,
    datetime_offset: args.offset,
    engine_local_iso: date.toISOString(),
    timezone_warning: args.offset
      ? null
      : "Input datetime has no explicit UTC offset; qfdk is being fed the venue-local wall time by convention.",
    purpose: args.purpose,
    location: args.location,
    basic_info: pan.basicInfo,
    si_zhu: pan.siZhu,
    ju_shu: pan.juShu,
    xun_shou: pan.xunShou,
    day_xun_shou: pan.dayXunShou,
    luo_gong_gan: pan.luoGongGan,
    zhi_fu: {
      gong: pan.zhiFuGong,
      yuan_gong: pan.zhiFuYuanGong,
      star: pan.zhiFuXing,
    },
    zhi_shi: {
      gong: pan.zhiShiGong,
      door: pan.zhiShiMen,
    },
    kong_wang_zhi: pan.kongWangZhi,
    kong_wang_gong: pan.kongWangGong,
    ma_star: pan.maStar,
    palaces,
    geju: pan.geju,
    analysis: pan.analysis,
    note: "Use qimen-scoring.md for football market scoring. qfdk provides chart structure; it does not itself produce betting picks.",
  };
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
  if (!args.datetime) {
    console.error("Missing --datetime.");
    console.error(usage());
    process.exit(2);
  }

  const engineDir = findEngineDir(args.engineDir);
  if (!engineDir) {
    console.log(
      JSON.stringify(
        {
          schema: "worldcup-mystic-oracle/qimen-qfdk-v1",
          status: "failed",
          reason: "qfdk/qimen engine not found. Provide --engine-dir or set QIMEN_QFDK_PATH.",
          engine_source: "https://github.com/qfdk/qimen",
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }

  const parsedDate = parseWallDate(args.datetime);
  if (!parsedDate || Number.isNaN(parsedDate.date.getTime())) {
    console.error(`Invalid --datetime: ${args.datetime}`);
    process.exit(2);
  }
  args.wallTime = parsedDate.wallTime;
  args.offset = parsedDate.offset;

  try {
    const qimen = require(path.join(engineDir, "lib", "qimen.js"));
    const pan = qimen.calculate(parsedDate.date, {
      method: args.method,
      purpose: args.purpose,
      location: args.location,
    });
    if (pan.error) {
      console.log(JSON.stringify({ status: "failed", engine: "qfdk/qimen", reason: pan.message, raw: pan }, null, 2));
      process.exit(1);
    }
    console.log(JSON.stringify(normalizePan(pan, args, engineDir, parsedDate.date), null, args.pretty ? 2 : 0));
  } catch (error) {
    console.log(
      JSON.stringify(
        {
          schema: "worldcup-mystic-oracle/qimen-qfdk-v1",
          status: "failed",
          engine: "qfdk/qimen",
          reason: error.message,
          hint: "Run npm install or pnpm install inside the qfdk/qimen engine directory, then retry.",
        },
        null,
        2,
      ),
    );
    process.exit(1);
  }
}

main();
