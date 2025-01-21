import os, sys, requests, pypdf, pymongo, gridfs

def getDocumentUrl(document_id: int) -> str:
    return f"https://dserver.bundestag.de/btd/{str(document_id)[0:2]}/{str(document_id)[2:5]}/{str(document_id)}.pdf"

def main(args: list[str]) -> int:
    if len(args) != 3:
        print(f"Usage: python3 {__file__} [start document] [end document]")
        return 0

    start_document = int(args[1])
    end_document = int(args[2])
    valid_document_urls = []

    #check documents for existance and size
    for i in range(start_document, end_document + 1):
        url = getDocumentUrl(i)
        result = requests.head(url)
        print(f"Analyzing document: {url} -> Code: {result.status_code}")

        if result.status_code == 200:
            valid_document_urls.append((url, int(result.headers["content-length"])))
    
    #calculate size
    total_size_b = 0
    for url in valid_document_urls: total_size_b += url[1]

    if total_size_b / (1024 ** 2) < 1000: 
        print(f"Calculated size of download: {float(total_size_b) / (1024.0 ** 2) :.2f} MiB")
    else: print(f"Calculated size of download: {float(total_size_b) / (1024.0 ** 3) :.2f} GiB")

    #

    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)