import fitz  # PyMuPDF
import json

def extract_toc_structure(file_path):
    pdf_document = fitz.open(file_path)
    toc = pdf_document.get_toc()    
    structure = {}
    for entry in toc:
        level, title, page_num = entry
        if level == 1:
            current_chapter = {
                "title": title,
                "sections": {},
                "text": ""
            }
            structure[str(len(structure) + 1)] = current_chapter
        elif level == 2:
            current_section = {
                "title": title,
                "subsections": {},
                "text": ""
            }
            structure[str(len(structure))]["sections"][str(len(structure[str(len(structure))]["sections"]) + 1)] = current_section
        elif level == 3:
            current_subsection = {
                "title": title,
                "text": ""
            }
            structure[str(len(structure))]["sections"][str(len(structure[str(len(structure))]["sections"]))]["subsections"][str(len(structure[str(len(structure))]["sections"][str(len(structure[str(len(structure))]["sections"]))]["subsections"]) + 1)] = current_subsection
    # print(structure)
    for chapter in structure.values():
        chapter_start_page = chapter.get("start_page", None)
        chapter_end_page = chapter.get("end_page", None)
        chapter["text"] = extract_text(pdf_document, chapter_start_page, chapter_end_page)
        for section in chapter["sections"].values():
            section_start_page = section.get("start_page", None)
            section_end_page = section.get("end_page", None)
            section["text"] = extract_text(pdf_document, section_start_page, section_end_page) 
            for subsection in section["subsections"].values():
                subsection_start_page = subsection.get("start_page", None)
                subsection_end_page = subsection.get("end_page", None)
                subsection["text"] = extract_text(pdf_document, subsection_start_page, subsection_end_page)
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


file_path = 'Руководство_Бухгалтерия_для_Узбекистана_ред_3_0.pdf'
output_file = 'structure.json'


# Extract structure and save to JSON
structure = extract_toc_structure(file_path)
save_structure_to_json(structure, output_file)
print(f'Structure saved to {output_file}')
