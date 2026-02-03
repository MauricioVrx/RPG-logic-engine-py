import pandas as pd

csv_dir   = f"data/info_csv/"
character = f"{csv_dir}character/"

# Character
df_char_class = pd.read_csv(f'{character}char_class.csv', sep = ';') 
df_background = pd.read_csv(f'{character}background.csv', sep = ';') 
df_ancestry   = pd.read_csv(f'{character}ancestry.csv'  , sep = ';')

# Info
df_trait      = pd.read_csv(f'{csv_dir}trait.csv', sep = ';') # Trait list


