import fs from "node:fs";
import path from "node:path";
import puppeteer from "puppeteer";
import { NextResponse } from "next/server";
import { renderNDADocumentHtml } from "@/lib/nda/renderDocument";
import { NDAFormData } from "@/lib/nda/types";

export const runtime = "nodejs";

export async function POST(request: Request) {
  let data: NDAFormData;
  try {
    data = await request.json();
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const documentHtml = renderNDADocumentHtml(data);
  const documentCss = fs.readFileSync(
    path.join(process.cwd(), "src", "styles", "nda-document.css"),
    "utf-8"
  );

  const html = `<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <style>${documentCss}</style>
  </head>
  <body>${documentHtml}</body>
</html>`;

  const browser = await puppeteer.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.setContent(html, { waitUntil: "load" });
    const pdf = await page.pdf({
      format: "letter",
      printBackground: true,
      margin: { top: "0.75in", bottom: "0.75in", left: "0.75in", right: "0.75in" },
    });

    return new NextResponse(Buffer.from(pdf), {
      status: 200,
      headers: {
        "Content-Type": "application/pdf",
        "Content-Disposition": 'attachment; filename="mutual-nda.pdf"',
      },
    });
  } finally {
    await browser.close();
  }
}
