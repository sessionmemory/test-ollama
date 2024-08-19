#!/usr/bin/env python3
# for testing local models responses on the droplet

"""
Module Docstring
"""

__author__ = "Alex Bishop"
__version__ = "0.3.0"
__license__ = "MIT"

# user_messages.py
import os
from config import *

# Basic Commands and Words
def msg_word_enter():
    return f"{BOLD_EFFECT}{STATS_COLOR}Enter{RESET_STYLE}"
def msg_word_select():
    return f"{BOLD_EFFECT}{STATS_COLOR}Select{RESET_STYLE}"
def msg_word_error():
    return f"{BOLD_EFFECT}{ERROR_COLOR}Error{RESET_STYLE}"
def msg_word_invalid():
    return f"Invalid"
def msg_word_model():
    return f"{BOLD_EFFECT}{MODEL_COLOR}model{RESET_STYLE}"
def msg_word_category():
    return f"{BOLD_EFFECT}{CATEGORY_COLOR}category{RESET_STYLE}"
def msg_word_prompt():
    return f"{BOLD_EFFECT}{PROMPT_COLOR}prompt{RESET_STYLE}"
def msg_word_number():
    return f"{BOLD_EFFECT}number{RESET_STYLE}"
def yes_or_no():
    return f"{BOLD_EFFECT}{STATS_COLOR}(y/n){RESET_STYLE}"

# Main Menu
def menu_option_single_prompt():
    return f"{PROMPT_COLOR}1.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu1_single}Single Prompt, Model, and Rate{RESET_STYLE} (Manual)"
def menu_option_model_prompt_selection():
    return f"{PROMPT_COLOR}2.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu2_prompt}Model & Prompt Selection{RESET_STYLE} (Sequence)"
def menu_option_model_category_selection():
    return f"{PROMPT_COLOR}3.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu3_category}Model & Category Selection{RESET_STYLE} (Sequence)"
def menu_option_all_prompts_single_model():
    return f"{PROMPT_COLOR}4.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu4_all}All Prompts to Single Model{RESET_STYLE} (Sequence)"
def menu_option_unsent_prompts():
    return f"{PROMPT_COLOR}5.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu5_unsent}Unsent Prompts for Model{RESET_STYLE} (Sequence)"
def menu_option_summary_prompts_excel():
    return f"{PROMPT_COLOR}6.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu6_summary}Summary Prompts on Excel{RESET_STYLE} (Sequence)"
def menu_option_query_completed_responses():
    return f"{PROMPT_COLOR}7.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu7_query}Query Completed Responses{RESET_STYLE}"
def menu_option_quit():
    return f"{PROMPT_COLOR}q.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu8_exit}Quit{RESET_STYLE}"

def menu_option_return_main():
    return f"{PROMPT_COLOR}m.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu_main}Return to Main Menu{RESET_STYLE}"
def menu_option_go_back():
    return f"{PROMPT_COLOR}b.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu_back}Go Back {RESET_STYLE}(Repeat this mode)"
def menu_option_quit_application():
    return f"{PROMPT_COLOR}q.{RESET_STYLE} {BOLD_EFFECT} {emoji_menu8_exit}Quit the application{RESET_STYLE}"

# User Interaction and Prompts
def msg_user_nudge():
    return f"{RESPONSE_COLOR}{BOLD_EFFECT}{emoji_user_nudge}{RESET_STYLE}"
def msg_multi_selection_input(action, items, extra_instruction=""):
    """
    Generates a message for multi-selection inputs.

    :param action: The action to be performed with the selected items (e.g., "send", "query").
    :param items: The items to select from.
    :param extra_instruction: Additional instructions or options (optional).
    :return: A formatted message string.
    """
    item_list = ", ".join([f"{item}" for item in items])
    return f"\n{msg_user_nudge()}{msg_word_select()} {msg_word_prompt()}s to {action} (or hit {BOLD_EFFECT}" + msg_word_select() + f"{RESET_STYLE} to {action} all): {extra_instruction}"

def msg_initial_mode():
    return f"\n{STATS_COLOR}{BOLD_EFFECT}" + msg_word_select() + f"{RESET_STYLE} a mode:"
def msg_msg_whats_next():
    return "\n" + msg_user_nudge() + "❓ What would you like to do next?"
def msg_go_back():
    return f"\n{PROMPT_COLOR}b.{RESET_STYLE} {BOLD_EFFECT}{emoji_menu_back}Back {RESET_STYLE}(Repeat this mode)"
def enter_your_choice():
    return msg_user_nudge() + msg_word_enter() + f" your choice: {RESET_STYLE}"
def msg_your_choice():
    return "\n" + msg_user_nudge() + "Your choice: "
def msg_confirm_selection():
    return f"\n{msg_user_nudge()}{STATS_COLOR}Please confirm your selection:{RESET_STYLE}" + yes_or_no() + ": "
def msg_farewell():
    return f"Bye now!" + f"{emoji_bye} {RESET_STYLE}"
def msg_number_1_10():
    return f"{msg_user_nudge()} {emoji_number} Please enter a {msg_word_number()} between 1 and 10."
def msg_save_response():
    return "\n" + msg_user_nudge() + f"Do you want to {BOLD_EFFECT}Save{RESET_STYLE} this response? " + yes_or_no() + ":"
def msg_select_y_n():
    return msg_user_nudge() + "Please " + msg_word_select() + " 'y' or 'n'."
def msg_q_to_quit():
    return msg_user_nudge() + msg_word_enter() + f" {STATS_COLOR}'q'{RESET_STYLE} to return to main menu."
def msg_get_response_rating():
    return "\n" + msg_user_nudge() + f"Rate the response on a scale of {PROMPT_COLOR}1 - 5{RESET_STYLE} (5 being the best):"
def msg_invalid_rating_num():
    return msg_word_invalid() + " rating, please " + msg_word_enter() + " a " + msg_word_number() + " between 1 and 5."
# Model Related
def msg_select_model_multiple():
    return f"\n{msg_user_nudge()}{msg_word_select()} the model(s) to use (e.g., 1-4, 5, 7), or type {STATS_COLOR}'q'{RESET_STYLE} to quit:\nYou can select multiple {msg_word_model()}s by separating {msg_word_number()}s with commas or specifying ranges (e.g., {BOLD_EFFECT}1-3,5{RESET_STYLE})."
def msg_select_model_single():
    return f"\n{msg_user_nudge()}{msg_word_select()} the model to use (e.g., 4), or type {STATS_COLOR}'q'{RESET_STYLE} to quit:"
def msg_enter_model_selection():
    return f"\n{msg_user_nudge()}{msg_word_enter()} your {msg_word_model()} selection: "
def msg_model_confirm(selected_models):
    return f"\n{msg_user_nudge()}{STATS_COLOR}You have selected: {BOLD_EFFECT}{MODELNAME_COLOR}{', '.join(selected_models)}{RESET_STYLE}"
def msg_use_same_model(selected_model):
    return f"\n{msg_user_nudge()}Do you want to continue with{RESET_STYLE} {BOLD_EFFECT}{MODELNAME_COLOR}{selected_model}{RESET_STYLE} {CONFIRM_COLOR}or select a different model? " + yes_or_no() + f": {RESET_STYLE}"
def msg_no_models():
    return f"{emoji_alert}No {msg_word_model()}s selected."

# Prompt Related
def msg_select_prompt_single():
    return f"\n" + msg_user_nudge() + msg_word_select() + " a " + msg_word_prompt() + ":"
def msg_enter_prompt_selection():
    return f"\n" + msg_user_nudge() + msg_word_enter() + " the " + msg_word_number() + " of the " + msg_word_prompt() + " you want to use: "
def msg_prompt_confirm(prompt):
    return f"\n{msg_user_nudge()}{STATS_COLOR}You have selected:{RESET_STYLE}\n- {PROMPT_SELECT_COLOR}{prompt}{RESET_STYLE}"
def msg_select_prompt_multiple():
    instruction = f"\n{msg_user_nudge()}{msg_word_select()} {msg_word_prompt()}(s):"
    input_prompt = f"\n{msg_user_nudge()}{msg_word_enter()} your choices: "
    return instruction, input_prompt
def msg_enter_prompt_selection_multiple():
    return f"\n{msg_user_nudge()}{msg_word_enter()} your choices (e.g., 1-3,5,7-8,10): "
def msg_enter_prompt_selection_single():
    return f"\n" + msg_user_nudge() + msg_word_enter() + " the " + msg_word_number() + " of the " + msg_word_prompt() + " you want to use: "
def msg_no_missing_prompts():
    return f"{emoji_alert}No missing {msg_word_prompt()}s for this {msg_word_model()}."
def msg_no_prompts():
    return f"{emoji_alert}No {msg_word_prompt()}s selected."
def msg_prompt_quantity():
    return f"{msg_user_nudge()} {emoji_number} {msg_word_enter()} the {msg_word_number()} of times to send each {msg_word_prompt()} (1-10): "
def msg_prompt_confirm_multi():
    return f"{STATS_COLOR}You have selected:{RESET_STYLE}"
def msg_list_selected_prompts(item):
    return f"- {PROMPT_SELECT_COLOR}{item}{RESET_STYLE}"

# Category Related
def msg_select_category():
    return f"\n" + msg_user_nudge() + msg_word_select() + " a " + msg_word_prompt() + " " + msg_word_category() + ":"
def msg_select_category_prompts(category_prompts):
    return f"\n" + msg_user_nudge() + msg_word_enter() + " your choices: ", category_prompts
def msg_prompts_from_category(selected_category):
    return f"\n" + msg_word_select() + " " + msg_word_prompt() + "s from the " + msg_word_category() + f" '{CATEGORY_COLOR}{selected_category}{RESET_STYLE}':"
def msg_select_prompt_from_cat(selected_category):
    f"\n" + msg_word_select() + " " + msg_word_prompt() + "s from the " + msg_word_category() + f" '{CATEGORY_COLOR}{selected_category}{RESET_STYLE}':"

# Use/Add Custom Prompt
def msg_custom_prompt_instr():
    return msg_user_nudge() + msg_word_enter() + f" '{PROMPT_COLOR}0{RESET_STYLE}' to enter a custom " + msg_word_prompt() + "."
def msg_enter_custom_prompt():
    return msg_word_enter() + " your custom " + msg_word_prompt() + ":"
def msg_add_custom_prompt_cat():
    return "\n" + msg_word_select() + " a " + msg_word_category() + " to add your " + msg_word_prompt() + " to:"
def msg_add_category_name():
    return "Or " + msg_word_select() + " a new " + msg_word_category() + " name."
def msg_enter_cat_name_num():
    return msg_word_enter() + " the " + msg_word_number() + " or name of the " + msg_word_category() + ": "
def msg_invalid_category():
    return msg_word_invalid() + " " + msg_word_category() + " " + msg_word_number() + ", creating a new " + msg_word_category() + "."
def msg_enter_category_num():
    return "\n" + msg_user_nudge() + msg_word_enter() + " the " + msg_word_number() + " of the " + msg_word_category() + " you want to use:"
def msg_confirm_custom_cat(selected_category):
    return msg_user_nudge() + "Confirm your " + msg_word_category() + f" selection '{CATEGORY_COLOR}{selected_category}{RESET_STYLE}'? " + yes_or_no() + ": "

# Message Content
def msg_sending_to_model(model_name, prompt):
    return f"\nSending " + msg_word_prompt() + " to " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}: {PROMPT_COLOR}{prompt}{RESET_STYLE}"
def msg_generating_msg(model_name, prompt):
    return f"\n{emoji_generating} Generating response for " + msg_word_model() + f": {BOLD_EFFECT}{MODELNAME_COLOR}{model_name}{RESET_STYLE} with " + msg_word_prompt() + f": {PROMPT_COLOR}{prompt}{RESET_STYLE}"
def msg_generating_selected(selected_model, prompt):
    return f"\n{emoji_generating} Generating response for " + msg_word_model() + f": {BOLD_EFFECT}{MODELNAME_COLOR}{selected_model}{RESET_STYLE} with " + msg_word_prompt() + f": {PROMPT_COLOR}{prompt}{RESET_STYLE}"
def msg_content(first_choice_content):
    return f"{RESPONSE_COLOR}{first_choice_content}{RESET_STYLE}"
def msg_no_resp_processing():
    return f"\n{emoji_alert}Response processing was not implemented for this {msg_word_model()}."

# Errors and Logs
def msg_invalid_returning():
    return f"{emoji_error}{msg_word_invalid()} option {emoji_error} Returning to the Main Menu!  {emoji_menu_main}"
def msg_invalid_response():
    return f"{emoji_error}No valid response generated."
def msg_invalid_retry():
    return f"{emoji_error} Invalid entry. Please enter a valid selection or type {STATS_COLOR}'q'{RESET_STYLE}. {msg_user_nudge}"
def msg_invalid_number():
    return f"{emoji_alert}{msg_word_invalid()} input {emoji_error} Please enter a {msg_word_number()} {emoji_number}."
def msg_invalid_number2(): 
    return msg_word_invalid() + " input, please " + msg_word_select() + " a single " + msg_word_number() + " without commas or dashes."
def msg_invalid_empty():
    return msg_word_prompt() + " cannot be empty, please try again."
def msg_valueerror():
    return "Selection out of range."
def msg_error_response(prompt, e):
    return f"{emoji_error}{msg_word_error} generating response for {msg_word_prompt} '{prompt}': {e}"
def msg_error_simple(e):
    return msg_word_error() + f" generating response: {str(e)}"
def msg_models_file_error(filename):
    return f"Models file {filename} not found."
def msg_no_response_file():
    return f"No response file found for " + msg_word_model() + " {model_name}."

# Summary Mode
def msg_select_summary_prompt():
    return f"\n{msg_user_nudge()}{STATS_COLOR}{msg_word_select()} a summarization {RESET_STYLE}{msg_word_prompt()}:"
def msg_summary_prompt_missing():
    return f"No " + msg_word_prompt() + f"s found for 'Comprehension and Summarization'. Please check your {BOLD_EFFECT}prompts.json{RESET_STYLE} file."
def msg_excel_completed(excel_path):
    return f"Updated Excel file saved to {excel_path}"
def msg_enter_prompt_num():
    return "\n" + msg_user_nudge() + msg_word_enter() + " the " + msg_word_number() + " of the " + msg_word_prompt() + " you want to use: "

# Query Mode
def msg_no_matching():
    return f"{emoji_alert}No matching responses found. 🙁"
def msg_found_unsent(missing_prompts, model_name):
    return f"\nFound {len(missing_prompts)} unsent " + msg_word_prompt() + "s for " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}."
def msg_sending_prompt(model_name, prompt):
    return f"\nSending {msg_word_prompt()} to {msg_word_model()} {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE}: {PROMPT_COLOR}{prompt}{RESET_STYLE}"
def msg_search_query(model_name, prompt):
    return f"\nSearching for responses from " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE} to " + msg_word_prompt() + f": {PROMPT_COLOR}{prompt}{RESET_STYLE}"
def msg_query_display_results(model_name, prompt, response):
    return f"\nResponse from " + msg_word_model() + f" {BOLD_EFFECT}{MODEL_COLOR}{model_name}{RESET_STYLE} to " + msg_word_prompt() + f" '{PROMPT_COLOR}{prompt}{RESET_STYLE}':\n{response['response']}"