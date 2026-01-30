import pandas as pd

csv_dir   = f"data/info_csv/"
equipment = f"{csv_dir}equipment/"
character = f"{csv_dir}character/"
item      = f"{csv_dir}item/"

# Character
df_char_class = pd.read_csv(f'{character}char_class.csv', sep = ';') 
df_background = pd.read_csv(f'{character}background.csv', sep = ';') 
df_ancestry   = pd.read_csv(f'{character}ancestry.csv'  , sep = ';')

# Equipment
df_armor   = pd.read_csv(f'{equipment}armor.csv' , sep = ';')
df_weapon  = pd.read_csv(f'{equipment}weapon.csv', sep = ';')
df_shield  = pd.read_csv(f'{equipment}shield.csv', sep = ';')

# Items
df_adventuring_gear = pd.read_csv(f'{item}adventuring_gear.csv', sep = ';')
df_consumables      = pd.read_csv(f'{item}consumables.csv', sep = ';')
__df_other_items    = ""

# Container
df_inventory   = ""
__df_temporary = ""

# Info
df_trait      = pd.read_csv(f'{csv_dir}trait.csv', sep = ';') # Trait list


