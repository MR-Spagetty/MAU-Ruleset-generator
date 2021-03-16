##
# MauRuleGenerator.py
# Grab a list of mau rules from an external file and pick a determined number
# of them at random

import os.path
import random
import requests


# Creating the list of possible cards
cards = ["♥", "♦", "♣", "♠", "A", "A♥", "A♦", "A♣", "A♠"]
for card in range(2, 11):
    cards.append(str(card))
    cards.append(f"{card}♥")
    cards.append(f"{card}♦")
    cards.append(f"{card}♣")
    cards.append(f"{card}♠")

cards.append("J")
cards.append("J♥")
cards.append("J♦")
cards.append("J♣")
cards.append("J♠")

cards.append("Q")
cards.append("Q♥")
cards.append("Q♦")
cards.append("Q♣")
cards.append("Q♠")

cards.append("K")
cards.append("K♥")
cards.append("K♦")
cards.append("K♣")
cards.append("K♠")

# Asking the user how many rules they want to have
not_valid = True
while not_valid:
    not_valid = False
    try:
        num_rules = int(input("How many rule would you like to have: "))
    except:
        not_valid = False

master_rulebook_git = ""
valid = True
try:
    master_rulebook_git = requests.get(
                                       "https://raw.githubusercontent.com/"
                                       "MR-Spagetty/MAU-Ruleset-generator/"
                                       "main/master_rule_book.txt")
except:
    valid = False
    print("Unable to access github Proceding with local master rulebook")
if valid:
    master_rule_book = open("MAU_RULE_BOOK.txt", "w")
    rulebook_backup = master_rulebook_git.text
    master_rule_book.writelines(rulebook_backup)
    master_rule_book.close()
    possible_rules_fixed = master_rulebook_git.text.split("\n")
    while "" in possible_rules_fixed:
        possible_rules_fixed.remove("")
    print(possible_rules_fixed)
else:
    if os.path.isfile("MAU_RULE_BOOK.txt"):
        master_rule_book = open("MAU_RULE_BOOK.txt", "r")
        possible_rules = master_rule_book.readlines()
        master_rule_book.close()
        possible_rules_fixed = []
        for rule in possible_rules:
            possible_rules_fixed.append(rule.strip("\n"))
    else:
        print("Master Rule book not found")
# Function to create a rule to add to the chosen rules list


def add_rule():
    slected_rule_id = random.randint(0, len(possible_rules_fixed) - 1)
    slected_card_id = random.randint(0, len(cards) - 1)
    chosen_rule = possible_rules_fixed[slected_rule_id]
    chosen_card = cards[slected_card_id]
    return chosen_rule, chosen_card

# Loop tp add the chosen rules to the chosen rulkes list one by one
chosen_rules = []
chosen_cards = []
for rule_num in range(num_rules):
    chosen_rule, chosen_card = add_rule()
    chosen_rules.append(chosen_rule)
    chosen_cards.append(chosen_card)
# Loop used to complete incomplete rules
for rule in chosen_rules:
    if ",choice" in rule:
        final_rule = []
        final_rule.append(rule.strip(",choice"))
        final_rule.append(input(f"Please finishe the rule:\n{final_rule[0]}"))
        chosen_rules[chosen_rules.index(rule)] = "".join(final_rule)


writeable_output = []
current_ruleset = open("CURRENT_RULES.txt", "w")
print("\nthe chosen rules are:")
for rule, card in zip(chosen_rules, chosen_cards):
    print(f"\n - {rule} = {card}")
    if "♥" in card:
        card = "".join([card.strip("♥"), " Hearts"])
    elif "♦" in card:
        card = "".join([card.strip("♦"), " Diamonds"])
    elif "♣" in card:
        card = "".join([card.strip("♣"), " Clubs"])
    elif "♠" in card:
        card = "".join([card.strip("♠"), " Spades"])
    item_to_write = " = ".join([rule, card])
    writeable_output.append("".join([item_to_write, "\n"]))

current_ruleset.writelines(writeable_output)
current_ruleset.close()
