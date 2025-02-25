import os, sys, time, json, pypdf, logging

def main(args = [], logger = None) -> int:
    start_time = time.time()

    try: os.mkdir("logs")
    except: pass

    logging.basicConfig(
        filename=f"logs/{time.strftime('%F_%T', time.localtime()).replace(':', '-')}.log",
        format=f"[%(levelname)s]%(message)s",
        level=logging.INFO
    )
    if logger == None: logger = logging.getLogger()

    if not os.path.isdir("btd"):
        logger.info(f"[{time.strftime('%F %T')}] No Documents to parse")
        return 0
    
    existant_documents = []
    documents_metadata = {}

    for file in os.listdir("btd"):
        if not str.endswith(file,".pdf"): continue
        existant_documents.append(file)
    existant_documents.sort()
    total_document_count = len(existant_documents)

    logger.info(f"[{time.strftime('%F %T')}] Working through input directory...")

    current_document_index = 1
    for document_path in existant_documents:
        completion_percentage = (float(current_document_index) / float(total_document_count)) * 100.0
        logger.info(f"[{time.strftime('%F %T')}] {completion_percentage :.2f}% - Reading document: {document_path}")
        
        with open(f"btd/{document_path}", "rb") as document_handle:
            document_reader = pypdf.PdfReader(document_handle)
            documents_metadata[document_path] = dict(document_reader.metadata)
            document_handle.close()
        current_document_index += 1

    with open("btd/metadata.json", "w") as metadata_handle:
        json.dump(documents_metadata, metadata_handle, indent=4)
        metadata_handle.close()

    logger.info(f"[{time.strftime('%F %T')}] Program finished in {time.time() - start_time :.1f} seconds.")
    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)