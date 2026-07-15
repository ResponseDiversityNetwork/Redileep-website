import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const dataDir = path.join(root, "data");
const outputDir = path.join(root, "outputs", "public_data");
const outputPath = path.join(outputDir, "redileep_public_data.xlsx");

const csvFiles = [
  "site_facts.csv",
  "partners.csv",
  "projects.csv",
  "work_packages.csv",
  "training_events.csv",
  "supervisors.csv",
  "deliverables.csv",
  "milestones.csv",
];

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let i = 0; i < text.length; i += 1) {
    const char = text[i];
    const next = text[i + 1];

    if (quoted) {
      if (char === '"' && next === '"') {
        field += '"';
        i += 1;
      } else if (char === '"') {
        quoted = false;
      } else {
        field += char;
      }
    } else if (char === '"') {
      quoted = true;
    } else if (char === ",") {
      row.push(field);
      field = "";
    } else if (char === "\n") {
      row.push(field);
      rows.push(row);
      row = [];
      field = "";
    } else if (char !== "\r") {
      field += char;
    }
  }

  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function sheetName(fileName) {
  return fileName
    .replace(".csv", "")
    .split("_")
    .map((word) => word[0].toUpperCase() + word.slice(1))
    .join(" ")
    .slice(0, 31);
}

function columnName(index) {
  let value = "";
  let n = index + 1;
  while (n > 0) {
    const rem = (n - 1) % 26;
    value = String.fromCharCode(65 + rem) + value;
    n = Math.floor((n - 1) / 26);
  }
  return value;
}

const workbook = Workbook.create();

for (const csvFile of csvFiles) {
  const text = await fs.readFile(path.join(dataDir, csvFile), "utf8");
  const rows = parseCsv(text);
  const sheet = workbook.worksheets.add(sheetName(csvFile));
  const rowCount = rows.length;
  const colCount = Math.max(...rows.map((row) => row.length));
  const padded = rows.map((row) => [...row, ...Array(colCount - row.length).fill("")]);
  const fullRange = sheet.getRange(`A1:${columnName(colCount - 1)}${rowCount}`);
  const headerRange = sheet.getRange(`A1:${columnName(colCount - 1)}1`);
  fullRange.values = padded;
  headerRange.format = {
    font: { bold: true, color: "#ffffff" },
    fill: "#244c5a",
  };
  fullRange.format = {
    verticalAlignment: "top",
    wrapText: true,
  };
  fullRange.format.autofitColumns();
  fullRange.format.autofitRows();
  sheet.freezePanes.freezeRows(1);
}

const summary = workbook.worksheets.add("Summary");
summary.getRange("A1:B5").values = [
  ["Workbook", "ReDiLEEP public website data"],
  ["Purpose", "Curated public reference extracts for the ReDiLEEP website"],
  ["Source handling", "Original PDFs remain local and ignored by Git"],
  ["Website content", "Visible page text is edited directly in the .qmd files; generated Markdown partials are no longer used"],
  ["Generated sheets", String(csvFiles.length)],
];
summary.getRange("A1:B1").format = {
  font: { bold: true, color: "#ffffff" },
  fill: "#244c5a",
};
summary.getRange("A1:B5").format = {
  verticalAlignment: "top",
  wrapText: true,
};
summary.getRange("A1:B5").format.autofitColumns();

await fs.mkdir(outputDir, { recursive: true });
const output = await SpreadsheetFile.exportXlsx(workbook);
await output.save(outputPath);
console.log(outputPath);
