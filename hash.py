import os, sys, time, json, hashlib, logging

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

    document_hashes = {}
    btd_documents = []

    btd_files = os.listdir("btd/")
    for file in btd_files:
        if file.endswith(".pdf"): btd_documents.append(file)
    btd_documents.sort()
    logger.info(f"[{time.strftime('%F %T')}] Found {len(btd_documents)} document(s).")
    
    logger.info(f"[{time.strftime('%F %T')}] Computing hash for...")
    documents_done = 1
    for document in btd_documents:
        if not document.endswith(".pdf"): continue
        with open("btd/" + document, 'rb') as document_handle:
            document_hash = hashlib.sha256(document_handle.read()).hexdigest()
            document_hashes[document] = document_hash
            logger.info(f"[{time.strftime('%F %T')}] ...{document} -> {document_hash} ({(documents_done / len(btd_documents)) * 100 :.2f}%)")
            documents_done += 1

    logger.info(f"[{time.strftime('%F %T')}] Writing hashes to 'hash.json'")
    with open("btd/hash.json", 'w') as hash_file_handle:
        json.dump(document_hashes, hash_file_handle, indent=4)

    logger.info(f"[{time.strftime('%F %T')}] Program finished in {time.time() - start_time :.1f} seconds.")
    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)