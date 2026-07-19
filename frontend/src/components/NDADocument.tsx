import { NDAFormData } from "@/lib/nda/types";
import { renderNDADocumentHtml } from "@/lib/nda/renderDocument";

export default function NDADocument({ data }: { data: NDAFormData }) {
  return <div dangerouslySetInnerHTML={{ __html: renderNDADocumentHtml(data) }} />;
}
