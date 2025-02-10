import os, sys, json, hashlib

def main(args: list) -> int:
    document_hashes = {}
    btd_documents = []

    btd_files = os.listdir("btd/")
    for file in btd_files:
        if file.endswith(".pdf"): btd_documents.append(file)
    print(f"Found {len(btd_documents)} document(s).")
    
    print("Computing hash for...")
    for document in btd_documents:
        if not document.endswith(".pdf"): continue
        with open("btd/" + document, 'rb') as document_handle:
            document_hash = hashlib.sha256(document_handle.read()).hexdigest()
            print(f"...{document} -> {document_hash}")
            document_hashes[document] = document_hash

    print("Writing hashes to 'hash.json'")
    with open("btd/hash.json", 'w') as hash_file_handle:
        json.dump(document_hashes, hash_file_handle, indent=4)

    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    sys.exit(exit_code)