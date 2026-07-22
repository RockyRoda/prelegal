export default function DocumentPreview({ html }: { html: string }) {
  if (!html) {
    return (
      <p className="text-sm text-zinc-500 dark:text-zinc-400">
        Tell the assistant what document you need to see a preview here.
      </p>
    );
  }

  return <div dangerouslySetInnerHTML={{ __html: html }} />;
}
