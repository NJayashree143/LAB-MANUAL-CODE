import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def clean_text(text):
    lines = text.split("\n")
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if re.match(r"^\d+\.\s*:$", line):
            continue
        if re.match(r"^\d+$", line):
            continue
        if re.match(r"^\:+$", line):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)

def extract_lab_programs(text):
    start_keywords = ["Laboratory Component", "Lab Section", "Programming Exercises:", "List of Experiments"]
    end_keywords = ["Teaching-Learning Process", "Course outcomes", "Assessment Details", "SEE for IC"]

    all_lab_programs = []
    start_indices = []

    for keyword in start_keywords:
        start_indices.extend([m.start() + len(keyword) for m in re.finditer(keyword, text, re.IGNORECASE)])

    if not start_indices:
        return ["No lab programs found."]

    start_indices.sort()

    for start_index in start_indices:
        end_index = len(text)
        for end_keyword in end_keywords:
            found_index = text.lower().find(end_keyword.lower(), start_index)
            if found_index != -1 and found_index < end_index:
                end_index = found_index
                break

        extracted_text = text[start_index:end_index].strip()
        extracted_text = clean_text(extracted_text)

        lab_programs = re.split(r"\n(?=\d+\.\s|\bDevelop|\bWrite|\bDesign|\bImplement|\bSimulate)", extracted_text)


        all_lab_programs.extend(lab_programs)


    cleaned_programs = []

    for i, prog in enumerate(all_lab_programs, 1):
        prog = re.sub(r"^\d+\.\s+", "", prog)
        cleaned_programs.append(f"{i}. {prog}")

    return cleaned_programs

pdf_path = "syl3.pdf"
text = extract_text_from_pdf(pdf_path)
print("!!!!!!!!111111111111111111111111111111111111111111111")
print(text)
lab_programs = extract_lab_programs(text)
print("@@@@@@@@@@@@@2222222222222222222222222222222222222222222")
print(len(lab_programs), type(lab_programs), lab_programs)


print("Extracted Lab Programs List:\n")
for program in lab_programs:
    print(program)
print()

with open("lab_programs.txt", "w", encoding="utf-8") as f:
    for program in lab_programs:
        f.write(program + "\n")
