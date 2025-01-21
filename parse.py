import os, sys, time, json, pypdf

def main(args: list[str]) -> int:
    start_time = time.time()

    if not os.path.isdir("btd"):
        print(f"[{time.strftime('%F %T')}] No Documents to parse")
        return 0
    
    existant_documents = []
    documents_metadata = {}

    for file in os.listdir("btd"):
        if not str.endswith(file,".pdf"): continue
        existant_documents.append(file)
    total_document_count = len(existant_documents)

    print(f"[{time.strftime('%F %T')}] Working through input directory...")

    current_document_index = 1
    for document_path in existant_documents:
        completion_percentage = (float(current_document_index) / float(total_document_count)) * 100.0
        print(f"[{time.strftime('%F %T')}] {completion_percentage :.2f}% - Reading document: {document_path}")
        
        with open(f"btd/{document_path}", "rb") as document_handle:
            document_reader = pypdf.PdfReader(document_handle)
            documents_metadata[document_path] = dict(document_reader.metadata)
            document_handle.close()
        current_document_index += 1

    with open("btd/metadata.json", "w") as metadata_handle:
        json.dump(documents_metadata, metadata_handle, indent=4)
        metadata_handle.close()

    print(f"[{time.strftime('%F %T')}] Program finished in {time.time() - start_time} seconds.")
    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)