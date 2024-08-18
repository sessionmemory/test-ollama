#!/usr/bin/env python3
# for testing local models responses on the droplet

"""
Module Docstring
"""

__author__ = "Alex Bishop"
__version__ = "0.3.0"
__license__ = "MIT"

# utils.py
import pandas as pd
import logging
from generation import generate
from config import MODEL_COLOR, CATEGORY_COLOR, PROMPT_COLOR, BOLD_EFFECT, RESET_STYLE, CONFIRM_COLOR, STATS_COLOR

def multi_selection_input(prompt, items):
    while True:
        print(prompt)
        for idx, item in enumerate(items, start=1):
            print(f"{idx}. {PROMPT_COLOR}{item}{RESET_STYLE}")
        selection_input = input("Enter your choices (e.g., 1-3,5,7-8,10): ").strip()

        # Process the input to support ranges
        selected_indices = []
        for part in selection_input.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                selected_indices.extend(range(start, end + 1))
            else:
                selected_indices.append(int(part))

        # Deduplicate and sort the indices
        selected_indices = sorted(set(selected_indices))

        # Validate selection
        try:
            selected_items = [items[idx - 1] for idx in selected_indices]
            print("You have selected: ")
            for item in selected_items:
                print(f"- {PROMPT_COLOR}{item}{RESET_STYLE}")
            if confirm_selection():
                return selected_items
        except (ValueError, IndexError):
            print("Invalid selection, please try again.")

def confirm_selection(message=f"Confirm your selection? {BOLD_EFFECT}{STATS_COLOR}(y/n){RESET_STYLE}: "):
    while True:
        confirm = input(message).strip().lower()
        if confirm == 'y':
            return True
        elif confirm == 'n':
            return False
        else:
            print("Please enter 'y' or 'n'.")

def select_category(categories):
    print("\nSelect a category:")
    for idx, category in enumerate(categories):
        print(f"{idx + 1}. {CATEGORY_COLOR}{category}{RESET_STYLE}")
    print(f"Enter '{PROMPT_COLOR}0{RESET_STYLE}' to enter a custom prompt.")
    print("Enter 'exit' to stop the program.")

    while True:
        category_input = input(f"{CONFIRM_COLOR}→ Enter the number of the {CATEGORY_COLOR}category{RESET_STYLE} you want to use: {RESET_STYLE}").strip()
        if category_input.lower() == 'exit':
            return None
        elif category_input == '':
            return [category['name'] for category in categories]  # Select all categories
        try:
            category_idx = int(category_input) - 1
            if category_idx == -1:
                selected_category = 'custom'
            elif 0 <= category_idx < len(categories):
                selected_category = categories[category_idx]
                # Confirmation step
                if not confirm_selection(f"Confirm your category selection '{CATEGORY_COLOR}{selected_category}{RESET_STYLE}'? {BOLD_EFFECT}{STATS_COLOR}(y/n){RESET_STYLE}: "):
                    print("Selection not confirmed. Please try again.")
                    return select_category(categories)  # Re-select if not confirmed
            else:
                print("Invalid category number, please try again.")
                return select_category(categories)
        except ValueError:
            print("Invalid input, please enter a number.")
            return select_category(categories)
        return selected_category
    
def print_response_stats(response, response_time, char_count, word_count):
    header_color = ""  # Bold and light yellow for header

    if response_time > 60:
        minutes = int(response_time // 60)
        seconds = int(response_time % 60)
        formatted_response_time = f"{minutes} minutes and {seconds} seconds"
    else:
        formatted_response_time = f"{response_time:.2f} seconds"

    print(f"\n{BOLD_EFFECT}{STATS_COLOR}Response Time:{RESET_STYLE} {formatted_response_time}")
    print(f"{BOLD_EFFECT}{STATS_COLOR}Character Count:{RESET_STYLE} {char_count}")
    print(f"{BOLD_EFFECT}{STATS_COLOR}Word Count:{RESET_STYLE} {word_count}")
    character_rate = char_count / response_time if response_time > 0 else 0
    word_rate = word_count / response_time if response_time > 0 else 0
    print(f"{BOLD_EFFECT}{STATS_COLOR}Character Rate:{RESET_STYLE} {character_rate:.2f} characters per second")
    print(f"{BOLD_EFFECT}{STATS_COLOR}Word Rate:{RESET_STYLE} {word_rate:.2f} words per second\n")

def get_user_rating():
    while True:
        rating = input(f"{CONFIRM_COLOR}→ Rate the response on a scale of {PROMPT_COLOR}1 - 5{RESET_STYLE} (5 being the best): {RESET_STYLE}").strip()
        try:
            rating = int(rating)
            if 1 <= rating <= 5:
                return rating
            else:
                print("Invalid rating, please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input, please enter a number.")

def process_excel_file(model_name, prompt, excel_path):
    # Load the Excel file
    df = pd.read_excel(excel_path, engine='openpyxl')

    # Define the new column name based on the model name
    summary_column_name = f"{model_name}-Summary"

    # Ensure the new summary column exists, if not, create it
    if summary_column_name not in df.columns:
        df[summary_column_name] = pd.Series(dtype='object')

    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        content = row['Message_Content']  # Assuming the content is in column B
        # Extract the first 15 words from the content
        first_15_words = ' '.join(content.split()[:15])
        
        # Print the message including the first 15 words of the content
        print(f"\nGenerating response for model {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE} with prompt - {PROMPT_COLOR}{prompt}{RESET_STYLE}")
        print(f"'{first_15_words}...'")
        
        # Generate the summary using the selected model and prompt
        try:
            _, response, _, _, _ = generate(model_name, f"{PROMPT_COLOR}{prompt}{RESET_STYLE} {content}", None)
        except Exception as e:
            logging.error(f"Error generating response for content: {e}")
            response = "Error generating response"
        # Prepend the prompt to the response
        full_response = f"{prompt}\n{response}"
        df.at[index, summary_column_name] = full_response  # Write the prompt and response to the new summary column
    
    # Save the modified DataFrame back to the Excel file
    df.to_excel(excel_path, index=False, engine='openpyxl')
    print(f"Updated Excel file saved to {excel_path}")