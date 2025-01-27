import os, sys, pypdf

def main(args: list) -> int:
    try: os.mkdir("./btd/text")
    except: pass

    documents = []
    for file in os.listdir("btd"):
        if file.endswith(".pdf"): documents.append(file)
    documents.sort()

    persist_line = False
    for document in documents:
        with open("btd/" + document, "rb") as document_handle:
            document_pdf = pypdf.PdfReader(document_handle)
            pages_text = [page.extract_text() for page in document_pdf.pages]
            for page_text in pages_text:
                for line_text in page_text.splitlines():
                    if line_text.strip() == "": continue
                    try:
                        if line_text[-1] == "-" and not line_text[-2].isspace(): print("Zeilentrenner!", document)
                    except: pass
                    #print(line_text)

    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)