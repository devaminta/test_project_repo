import fitz  # PyMuPDF
import json

def extract_toc_structure(file_path):
    pdf_document = fitz.open(file_path)
    toc = pdf_document.get_toc()
    structure = {}
    chapter_num = section_num = subsection_num = 0

    for entry in toc:
        level, title, page_num = entry

        if level == 1:
            chapter_num += 1
            section_num = subsection_num = 0
            chapter_key = str(chapter_num)
            chapter = {
                "title": title,
                "sections": {}
            }
            structure[chapter_key] = chapter

        elif level == 2:
            if chapter_num == 0:
                continue
            section_num += 1
            subsection_num = 0
            section_key = f"{chapter_num}.{section_num}"
            section = {
                "title": title,
                "subsections": {}
            }
            structure[str(chapter_num)]["sections"][section_key] = section

        elif level == 3:
            if chapter_num == 0 or section_num == 0:
                continue
            subsection_num += 1
            subsection_key = f"{chapter_num}.{section_num}.{subsection_num}"
            subsection = {
                "title": title
            }
            structure[str(chapter_num)]["sections"][f"{chapter_num}.{section_num}"]["subsections"][subsection_key] = subsection

    return structure

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
