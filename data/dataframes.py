import pandas as pd

csv_dir = "data/info_csv/"

# Character
df_char_class = pd.read_csv(f'{csv_dir}char_class.csv', sep = ';') 
df_background = pd.read_csv(f'{csv_dir}background.csv', sep = ';') 
df_ancestry   = pd.read_csv(f'{csv_dir}ancestry.csv', sep = ';')

# Entity
df_armor      = pd.read_csv(f'{csv_dir}armor.csv', sep = ';')

# Info
df_trait      = pd.read_csv(f'{csv_dir}trait.csv', sep = ';') # Trait list


