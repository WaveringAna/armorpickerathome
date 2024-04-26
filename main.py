class ArmorPiece:
    def __init__(self, name, armor_hash, armor_id, tier, type, source, equippable, mobility, resilience, recovery, discipline, intellect, strength, total):  # Include other attributes if needed
        self.name = name
        self.armor_hash = armor_hash
        self.armor_id = armor_id
        self.tier = tier
        self.type = type  # Helmet, Arms, etc.
        self.source = source
        self.equippable = equippable
        self.mobility = mobility
        self.resilience = resilience
        self.recovery = recovery
        self.discipline = discipline
        self.intellect = intellect
        self.strength = strength
        self.total = total

class Character:
    def __init__(self, name, class_type):
        self.name = name
        self.class_type = class_type
        self.helmet = None
        self.arms = None
        self.chest = None
        self.legs = None
        self.class_item = None

import csv

def load_armor_data(csv_file):
    armor_pieces = []
    with open(csv_file, 'r', encoding="utf8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            armor_pieces.append(ArmorPiece(row['Name'], row['Hash'], row['Id'], row['Tier'], row['Type'], row['Source'], row['Equippable'], int(row['Mobility']), int(row['Resilience']), int(row['Recovery']), int(row['Discipline']), int(row['Intellect']), int(row['Strength']), int(row['Total'])))
    return armor_pieces

def equip_armor(character, armor_piece):
    classtype = character.class_type.lower()  # Convert to lowercase for matching
    print
    if armor_piece.equippable.lower() != classtype:
        print("Invalid armor type for this character")
        print("Expected: " + classtype)
        print("Received: " + armor_piece.equippable.lower())
        print("Armor piece: " + armor_piece.name)
        return

    slot = armor_piece.type.lower()  # Convert to lowercase for matching
    if slot == 'helmet':
        character.helmet = armor_piece
    elif slot == 'gauntlets':
        character.arms = armor_piece
    elif slot == 'chest armor':
        character.chest = armor_piece
    elif slot == 'leg armor':
        character.legs = armor_piece
    elif slot == 'warlock bond' or 'hunter cloak' or 'titan mark':
        character.class_item = armor_piece
    else:
        print("Invalid armor slot")
        print("Expected: Helmet, Gauntlets, Chest Armor, Leg Armor, Warlock Bond, Hunter Cloak, Titan Mark")
        print("Received: " + slot)
        print("Armor piece: " + armor_piece.name)

def calculate_character_stats(character):
    stats = {
        'mobility': 0,
        'resilience': 0,
        'recovery': 0,
        'discipline': 0,
        'intellect': 0,
        'strength': 0,
        'total': 0
    }

    for armor in [character.helmet, character.arms, character.chest, character.legs, character.class_item]:
        if armor:  # Check if armor piece exists
            stats['mobility'] += armor.mobility
            stats['resilience'] += armor.resilience
            stats['recovery'] += armor.recovery
            stats['discipline'] += armor.discipline
            stats['intellect'] += armor.intellect
            stats['strength'] += armor.strength
            stats['total'] += armor.total
             # ... and so on
    return stats

armor_data = load_armor_data('destinyArmor.csv')

my_hunter = Character('My Hunter', 'Hunter')

from itertools import combinations

def find_valid_combinations(armor_data, character, *target_stat, **target_value):
    """
    Finds all valid armor combinations for a given character, considering class restrictions.

    Args:
        armor_data: A list of ArmorPiece objects.
        character: A Character object.
        target_stat: The stat to optimize for (e.g., 'mobility', 'resilience', 'recovery', 'discipline', 'intellect', 'strength').
        target_value: The target value for the optimization stat.

    Returns:
        A list of valid combinations, where each combination is a tuple of 5 ArmorPiece objects:
        (helmet, arms, chest, legs, class_item)
    """

    valid_combinations = []

    # Filter armor by character class
    class_specific_armor = [piece for piece in armor_data if piece.equippable.lower() == character.class_type.lower()]

    # Generate all possible combinations (order matters for armor slots)
    for combo in combinations(class_specific_armor, 5):
        if (combo[0].type.lower() == 'helmet' and
            combo[1].type.lower() == 'gauntlets' and
            combo[2].type.lower() == 'chest armor' and
            combo[3].type.lower() == 'leg armor' and
           (combo[4].type.lower() == 'warlock bond' or 
            combo[4].type.lower() == 'hunter cloak' or 
            combo[4].type.lower() == 'titan mark')):
            valid_combinations.append(combo)

        if (target_stat and target_value):
            total_stat = sum(piece.target_stat for piece in combo)
            if total_stat == target_value:
                valid_combinations.append(combo)

    return valid_combinations

hunter_combinations = find_valid_combinations(armor_data, my_hunter, "mobility", 100)

if hunter_combinations:
    # Print armor combinations
    for combo in hunter_combinations:
        print("Helmet:", combo[0].name)
        print("Arms:", combo[1].name)
        # ... and so on for the other pieces
        print("-" * 20)  # Separator between combinations
else:
    print("No combinations found that meet the target mobility of 100.")
