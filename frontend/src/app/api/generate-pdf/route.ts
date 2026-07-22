import fs from "node:fs";
import path from "node:path";
import puppeteer from "puppeteer";
import { NextResponse } from "next/server";

export const runtime = "nodejs";

const BACKEND_INTERNAL_URL = process.env.BACKEND_INTERNAL_URL ?? "http://localhost:8000";

export async function POST(request: Request) {
  let docId: string;
  let fieldValues: Record<string, string>;
  try {
    const body = await request.json();
    docId = body.docId;
    fieldValues = body.fieldValues ?? {};
    if (!docId) throw new Error("Missing docId");
  } catch {
    return NextResponse.json({ error: "Invalid JSON body" }, { status: 400 });
  }

  const renderResponse = await fetch(`${BACKEND_INTERNAL_URL}/api/documents/${docId}/render`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ fieldValues }),
  });

  if (!renderResponse.ok) {
    return NextResponse.json({ error: "Failed to render document" }, { status: renderResponse.status });
  }

  const { html: documentHtml } = (await renderResponse.json()) as { html: string };
  const documentCss = fs.readFileSync(
    path.join(process.cwd(), "src", "styles", "document.css"),
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

  // Docker's default container runtime blocks the namespace syscalls
  // Chromium's sandbox needs, so it must be disabled to launch at all.
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });
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
        "Content-Disposition": `attachment; filename="${docId}.pdf"`,
      },
    });
  } finally {
    await browser.close();
  }
}
