import fitz  # PyMuPDF
import json

def extract_toc_structure(file_path):
    pdf_document = fitz.open(file_path)
    toc = pdf_document.get_toc()    
    structure = {}
    chapter = section = subsection = None

    for entry in toc:
        level, title, page_num = entry

        if level == 1:
            chapter = {
                "title": title,
                "sections": {},
                "text": ""
            }
            structure[str(len(structure) + 1)] = chapter

        elif level == 2 and chapter:
            section = {
                "title": title,
                "subsections": {},
                "text": ""
            }
            chapter["sections"][str(len(chapter["sections"]) + 1)] = section

        elif level == 3 and section:
            subsection = {
                "title": title,
                "text": ""
            }
            section["subsections"][str(len(section["subsections"]) + 1)] = subsection

    for chapter_key, chapter in structure.items():
        chapter["text"] = extract_text(pdf_document, chapter.get("start_page"), chapter.get("end_page"))
        for section_key, section in chapter["sections"].items():
            section["text"] = extract_text(pdf_document, section.get("start_page"), section.get("end_page"))
            for subsection_key, subsection in section["subsections"].items():
                subsection["text"] = extract_text(pdf_document, subsection.get("start_page"), subsection.get("end_page"))

    return structure

def extract_text(pdf_document, start_page, end_page):
    text = ""
    if start_page is not None and end_page is not None:
        for page_num in range(start_page - 1, end_page):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def save_structure_to_json(structure, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, ensure_ascii=False, indent=4)

# Set file paths
file_path = 'Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf'
output_file = 'structure.json'

# Extract structure and save to JSON
structure = extract_toc_structure(file_path)
save_structure_to_json(structure, output_file)
print(f'Structure saved to {output_file}')
