import os, sys, time, json, hashlib

def main(args: list) -> int:
    start_time = time.time()
    document_hashes = {}
    btd_documents = []

    btd_files = os.listdir("btd/")
    for file in btd_files:
        if file.endswith(".pdf"): btd_documents.append(file)
    btd_documents.sort()
    print(f"[{time.strftime('%F %T')}] Found {len(btd_documents)} document(s).")
    
    print(f"[{time.strftime('%F %T')}] Computing hash for...")
    documents_done = 1
    for document in btd_documents:
        if not document.endswith(".pdf"): continue
        with open("btd/" + document, 'rb') as document_handle:
            document_hash = hashlib.sha256(document_handle.read()).hexdigest()
            document_hashes[document] = document_hash
            print(f"[{time.strftime('%F %T')}] ...{document} -> {document_hash} ({(documents_done / len(btd_documents)) * 100 :.2f}%)")
            documents_done += 1

    print(f"[{time.strftime('%F %T')}] Writing hashes to 'hash.json'")
    with open("btd/hash.json", 'w') as hash_file_handle:
        json.dump(document_hashes, hash_file_handle, indent=4)

    print(f"[{time.strftime('%F %T')}] Program finished in {time.time() - start_time :.1f} seconds.")
    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)