from characterconversion import MORSE_CODE_DICT

def text_to_morse(text: str) -> str:
    morse_output = []
    for char in text.upper():
        if char in MORSE_CODE_DICT:
            morse_output.append(MORSE_CODE_DICT[char])
        else:
            morse_output.append('?')
    return ' '.join(morse_output)

def main():
    print("=== Morse Code Converter ===")
    user_input = input("Enter text to convert to Morse code: ")
    morse_code = text_to_morse(user_input)
    print(f"\nMorse Code:\n{morse_code}")

if __name__ == "__main__":
    main()