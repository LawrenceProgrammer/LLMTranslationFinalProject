import os
import requests
import sacrebleu
import xml.etree.ElementTree as ET
from utils.llm import translate_util

FLORES_BASE_URL = "https://raw.githubusercontent.com/christos-c/bible-corpus/refs/heads/master/bibles/"
ENGLISH_REFERENCE_URL = f"{FLORES_BASE_URL}English.xml"
FRENCH_REFERENCE_URL = f"{FLORES_BASE_URL}French.xml"
CHINESE_REFERENCE_URL = f"{FLORES_BASE_URL}Chinese.xml"

def download_file(url, destination):
    """
    Download a file from a URL to a destination.
    """
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(destination, 'wb') as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded: {destination}")
    else:
        raise Exception(f"Failed to download {url}. HTTP Status Code: {response.status_code}")

def calculate_bleu(reference_texts, candidate_texts):
    """
    Calculate BLEU score using sacrebleu.

    Args:
        reference_texts (list of str): List of reference translations.
        candidate_texts (list of str): List of candidate translations.

    Returns:
        float: BLEU score.
    """
    bleu = sacrebleu.corpus_bleu(candidate_texts, [reference_texts])
    return bleu.score

def compute_chr_score(reference_texts, candidate_texts):
    """
    Compute the CHR score for translations.

    Args:
        reference_texts (list of str): List of reference translations.
        candidate_texts (list of str): List of candidate translations.

    Returns:
        float: CHR score.
    """
    if len(reference_texts) != len(candidate_texts):
        raise ValueError("The number of reference texts and candidate texts must be equal.")

    # Use sacrebleu to compute CHR score
    chr_score = sacrebleu.corpus_chrf(candidate_texts, [reference_texts])
    return chr_score.score

def process_text_file(file_path):
    """
    Read a file line by line and return a list of lines.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return [line.strip() for line in file.readlines()]

def process_file(file_path):
    sentences = []
    try:
        # Parse the XML file
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Search for all <seg> tags
        for seg in root.findall(".//seg"):
            text = seg.text.strip() if seg.text else ""
            if text:
                sentences.append(text)
    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
    return sentences

def append_to_file(filename, content):
    """
    Appends content to the specified file.
    
    Args:
        filename (str): The file to append to.
        content (str): The content to write.
    """
    try:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(content + "\n")  # Append the content with a newline
        print(f"Successfully appended content to {filename}")
    except Exception as e:
        print(f"Error writing to file {filename}: {e}")

def main():
    # Define file paths
    english_file = "english.xml"
    french_file = "french.xml"
    chinese_file = "chinese.xml"

    # Download the files if not already present
    if not os.path.exists(english_file):
        print("Downloading reference translations...")
        download_file(ENGLISH_REFERENCE_URL, english_file)

    if not os.path.exists(french_file):
        print("Downloading french translations...")
        download_file(ENGLISH_REFERENCE_URL, french_file)

    if not os.path.exists(chinese_file):
        print("Downloading chinese translations...")
        download_file(ENGLISH_REFERENCE_URL, chinese_file)

    # Process the files
    print("Processing files...")
    english_text = process_file(english_file)
    dest_language_texts = {
        "French": process_file(french_file),
        "Chinese": process_file(chinese_file)
    }

    llms = [
        "gpt-4o",
        "gpt-4o-mini",
        "gpt-3.5-turbo",
        "mistral-large-latest",
        "mistral-small-latest"
    ]
    
    languages = [
        "French",
        "Chinese"
    ]

    num_translations = 100

    for llm in llms:
        for language in languages:
            reference_texts = []
            destination_texts = []
            print("Translating from English to", language, "...")
            for i in range(0, num_translations):
                try:
                    translation = translate_util(english_text[i], "English", language, llm)
                    translation_text = translation["translation"]
                    # print(reference_texts[i], translation_text)
                    reference_texts.append(dest_language_texts[language][i])
                    destination_texts.append(translation_text)
                except:
                    pass

            # Calculate BLEU score
            print("Calculating BLEU score...")
            bleu_score = calculate_bleu(reference_texts, destination_texts) * 100.0
            print(f"BLEU Score: {bleu_score:.2f}")

            # Calculate CHRF score
            print("Calculating CHRF score...")
            chr_score = compute_chr_score(reference_texts, destination_texts)
            print(f"CHR Score: {chr_score:.2f}")

            append_to_file("report.txt", f"{llm}: English to {language}: BLEU Score: {bleu_score:.2f}, CHR Score: {chr_score:.2f}")

if __name__ == "__main__":
    main()
