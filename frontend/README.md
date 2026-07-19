# Mutual NDA Creator

A prototype web app for [PL-3](https://imyth-x.atlassian.net/browse/PL-3): fill in a form with the key details of a Mutual Non-Disclosure Agreement, see it assembled live, and download it as a PDF.

The generated document is based on the [Common Paper Mutual NDA](https://commonpaper.com/standards/mutual-nda/1.0/) (Version 1.0, CC BY 4.0) — the Standard Terms and Cover Page fields from `../templates/Mutual-NDA.md` and `../templates/Mutual-NDA-coverpage.md` at the repo root.

## How it works

- `src/lib/nda/` — the content model: form data types, defaults, term-resolution logic, and `renderNDADocumentHtml()`, which renders the full agreement (cover page + standard terms) to an HTML string.
- `src/components/NDADocument.tsx` — renders that HTML string for the on-screen live preview.
- `src/app/api/generate-pdf/route.ts` — a Route Handler that renders the same HTML string, feeds it to headless Chromium via [Puppeteer](https://pptr.dev), and streams back a PDF. Because the preview and the PDF share one rendering function, they never drift apart.

## Getting Started

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000). The first `npm install` also downloads a local Chromium build for Puppeteer, so it may take a minute.

## Scripts

- `npm run dev` — start the dev server
- `npm run build` — production build
- `npm run start` — run the production build
- `npm run lint` — ESLint
