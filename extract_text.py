import fitz
import os

def extract_text_from_pdfs(pdf_folder):
    all_texts = []
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            doc = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            all_texts.append({"filename": filename, "content": text})
            
    return all_texts

def write_files_to_file(directory, output_file):
    with open(output_file, 'w') as f:
        for root, dirs, files in os.walk(directory):
            for file in files:
                f.write(os.path.join(root, file) + '\n ')

def extract_and_save_text(pdf_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    all_texts = []
    
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            path = os.path.join(pdf_folder, filename)
            doc  = fitz.open(path)
            text = ""
            for page in doc:
                text += page.get_text()
            
            #Saving to a text file
            txt_filename = os.path.splitext(filename)[0] + ".txt"
            with open(os.path.join(output_folder, txt_filename), "w", encoding="utf-8") as f:
                f.write(text)
            
            all_texts.append({"filename": filename, "content": text})
    return all_texts

pdf_folder = "C:/Users/CDevlin/Documents/browning_ai/PDFs"

#docs = extract_text_from_pdfs(pdf_folder)

write_files_to_file(pdf_folder, "files.txt")

docs = extract_and_save_text(pdf_folder, "C:/Users/CDevlin/Documents/browning_ai/PDFs_txts")