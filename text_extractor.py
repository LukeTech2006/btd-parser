import os, sys, pypdf

def main(args: list) -> int:
    try: os.mkdir("./btd/text")
    except: pass

    documents = []
    for file in os.listdir("btd"):
        if file.endswith(".pdf"): documents.append(file)
    documents.sort()

    skip_next = False
    parsed_lines = []
    for document in documents:
        with open("btd/"+document, "rb") as document_handle:
            document_pdf = pypdf.PdfReader(document_handle)
            document_pages = [page.extract_text() for page in document_pdf.pages]

            for i in range(document_pages.__len__()):
                document_page_lines = document_pages[i].splitlines()
                for j in range(document_page_lines.__len__()):
                    line = document_page_lines[j]

                    if skip_next:
                        skip_next = False
                        continue

                    if line.strip() == "": continue
                    line = line.strip()
                    
                    try:
                        print("Zeile:", j, line[-1], line[-2])
                        if line[-1] == "-" and (not line[-2].isspace()):
                            parsed_lines.append(line[:-1] + document_page_lines[j+1])
                            skip_next = True
                            print("Zeilentrenner in Zeile", j)
                            continue
                    except: pass

                    parsed_lines.append(line)

        with open("btd/text/"+document[:-4]+".txt", "w") as text_file_handle:
            text_file_handle.write("\n".join(parsed_lines))

    return 0

if __name__ == "__main__":
    exit_code = main(sys.argv)
    os._exit(exit_code)