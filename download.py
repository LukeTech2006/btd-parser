import os, sys, time, hashlib, requests

def getDocumentUrl(document_id: int) -> str:
    document_id_s = str(document_id).zfill(7)
    return f"https://dserver.bundestag.de/btd/{str(document_id_s)[0:2]}/{str(document_id_s)[2:5]}/{str(document_id_s)}.pdf"

def main(args: list) -> int:
    if len(args) != 3:
        print(f"Usage: python3 {__file__} [start document] [end document]")
        return 0

    if os.path.isdir("btd"):
        existant_documents = os.listdir("btd/")
    else: existant_documents = []

    existant_documents_hashes = {}
    valid_document_urls = []

    start_time = time.time()
    start_document = int(args[1])
    end_document = int(args[2])
    total_size_b = 0

    #calculate hashes of existing documents
    print(f"[{time.strftime('%F %T')}] Generating hash-lookup...", end="")
    for existant_document in existant_documents:
        with open(f"btd/{existant_document}", "rb") as existant_document_handle:
            existant_document_hash = hashlib.sha256(existant_document_handle.read())
            existant_documents_hashes[existant_document] = existant_document_hash.hexdigest()
    print("Done.")

    #check documents for existance on remote location
    missing_documents = 0
    for i in range(start_document, end_document + 1):
        url = getDocumentUrl(i)
        try: result = requests.head(url)
        except: continue
        completion_percentage = (float(i + 1 - start_document) / float((end_document + 1) - start_document)) * 100.0
        print(f"[{time.strftime('%F %T')}] {completion_percentage :.2f}% - Checking remote document: {url} -> Code: {result.status_code}")

        if result.status_code == 200:
            missing_documents = 0
            valid_document_urls.append(url)
            total_size_b += int(result.headers["content-length"])
        else: missing_documents += 1

        if missing_documents >= 100: break

    #calculate size
    if total_size_b / (1024 ** 2) < 1024: 
        print(f"[{time.strftime('%F %T')}] Calculated size of download: {float(total_size_b) / (1024.0 ** 2) :.2f} MiB")
    else:
        print(f"[{time.strftime('%F %T')}] Calculated size of download: {float(total_size_b) / (1024.0 ** 3) :.2f} GiB")

    #download documents
    try: os.mkdir("btd")
    except: pass

    download_size = 0
    new_documents = 0
    updated_documents = 0
    skipped_documents = 0
    for document_url in valid_document_urls:
        try: document = requests.get(document_url)
        except: continue
        download_size += int(document.headers["content-length"])
        completion_percentage = (float(download_size) / float(total_size_b)) * 100.0

        document_digested_title = "Drucksache_" + document_url[-11:-9] + "-" + document_url[-9:-4]
        document_filename = document_digested_title.replace("/", "-").replace(" ", "_") + ".pdf"

        document_updated = True
        hash_newfile = hashlib.sha256(document.content).hexdigest()
        for existant_document in existant_documents:
            hash_oldfile = existant_documents_hashes[existant_document]
            if hash_oldfile == hash_newfile:
                document_updated = False
                break

        if document_updated:
            #put/overwrite document
            if os.path.exists(f"btd/{document_filename}"): updated_documents += 1
            else: new_documents += 1

            with open(f"btd/{document_filename}", 'wb+') as document_file:
                document_file.write(document.content)
                document_file.close()

            print(f"[{time.strftime('%F %T')}] {completion_percentage :.2f}% - Downloaded document: {document_digested_title}")
        else:
            skipped_documents += 1
            print(f"[{time.strftime('%F %T')}] {completion_percentage :.2f}% - Skipped document: {document_digested_title}")

    print(f"[{time.strftime('%F %T')}] Program finished in {time.time() - start_time :.1f} seconds.")
    print(f"[{time.strftime('%F %T')}] {new_documents} Document(s) new; {updated_documents} Document(s) updated; {skipped_documents} Document(s) skipped")
    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)
