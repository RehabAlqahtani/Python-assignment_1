import re
from itertools import combinations

def main():
    # Reading letter values from a text file
    with open('Rhb_values.txt', 'r') as value_file:
        letter_data = value_file.readlines()
    # Creating a dictionary to map letters to their corresponding values
    value_dictionary = {line.split()[0]: int(line.split()[1]) for line in letter_data}

    # Opening and reading names from the input file
    input_path = 'Rhb_file.txt'
    with open(input_path, 'r') as file_handler:
        name_list = file_handler.read().splitlines()

    # Preparing to write the output to a file
    output_path = 'output_abbrevsfinal.txt'
    with open(output_path, 'w') as output_file:
        # Process each name in the list
        for current_name in name_list:
            # Remove non-alphabetic characters and convert to uppercase
            sanitized_name = re.sub(r"[^a-zA-Z\s]", "", current_name).upper()
            # Split the name into words and join them to form a concatenated string
            name_parts = sanitized_name.split()
            joined_name = "".join(name_parts)
            # Generate two-letter combinations of indices, including the first letter
            name_combinations = combinations(range(1, len(joined_name)), 2)
            name_combinations = [(0, *combo) for combo in name_combinations]

            # Initialize a dictionary to keep track of scores for each combination
            score_map = {}
            # Score each combination
            for combo in name_combinations:
                combo_score = 0
                word_index = 0
                for word in sanitized_name.split():
                    for idx in combo:
                        if word_index <= idx < word_index + len(word):
                            relative_idx = idx - word_index
                            # Calculate score based on letter position in the word
                            if relative_idx == 0:
                                combo_score += 0
                            elif relative_idx == len(word) - 1:
                                combo_score += 20 if word[relative_idx] == 'E' else 5
                            else:
                                position_score = 1 if relative_idx == 1 else 2 if relative_idx == 2 else 3
                                combo_score += position_score + value_dictionary.get(word[relative_idx], 0)
                    word_index += len(word)
                # Store the calculated score
                score_map[''.join(joined_name[i] for i in combo)] = combo_score

            # Determine the minimum score among all combinations
            minimum_score = min(score_map.values())
            # Select combinations that have the minimum score
            best_combos = [abbr for abbr, scr in score_map.items() if scr == minimum_score]
            
            # Write the name and its best abbreviations to the output file
            output_file.write(current_name + '\n')
            output_file.write(' '.join(best_combos) + '\n')

if __name__ == "__main__":
    main()