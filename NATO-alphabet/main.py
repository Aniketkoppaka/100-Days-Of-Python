import pandas

# Load NATO phonetic alphabet data from CSV
data = pandas.read_csv("nato_phonetic_alphabet.csv")

# Create a dictionary mapping letters to phonetic codes
phonetic_dict = {row.letter: row.code for (index, row) in data.iterrows()}

# Function to generate phonetic code for a given word
def generate_phonetic():
    word = input("Enter a word: ").upper()
    try:
        # Convert each letter in the word to its phonetic code
        output_list = [phonetic_dict[letter] for letter in word]
    except KeyError:
        # Handle invalid characters (non-alphabet input)
        print("Sorry, only letters in the alphabet please.")
        generate_phonetic()
    else:
        # Print the resulting phonetic code list
        print(output_list)

# Start the program
generate_phonetic()
