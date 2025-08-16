import pdfplumber
from gtts import gTTS
import os

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' was not found.")
        return None

    print("Starting text extraction from PDF...")
    full_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"The PDF has {total_pages} pages.")

            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                print(f"Processed page {i+1}/{total_pages}.")

        print("Text extraction complete.")
        return full_text
    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")
        return None

def convert_text_to_speech(text, output_filename, language="en"):
    if not text.strip():
        print("The extracted text is empty. Cannot generate audio.")
        return

    print("Starting text-to-speech conversion...")
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(output_filename)
        print(f"Successfully created audiobook! It's saved as '{output_filename}'")
    except Exception as e:
        print(f"An error occurred during text-to-speech conversion: {e}")

def main():
    print("--- PDF to Audiobook Converter ---")
    pdf_file = input("Please enter the full path to your PDF file: ")
    output_audio_file = input("Please enter the desired name for the output audio file (e.g., my_audiobook.mp3): ")

    if not output_audio_file.lower().endswith('.mp3'):
        output_audio_file += '.mp3'

    extracted_text = extract_text_from_pdf(pdf_file)

    if extracted_text:
        convert_text_to_speech(extracted_text, output_audio_file)
    else:
        print("Could not proceed with audio conversion due to an error in text extraction.")

if __name__ == "__main__":
    main()