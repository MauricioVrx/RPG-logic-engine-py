import math
from scripts.exceptions import (
    DataFrameMultipleRowsError,
    DataFrameRowNotFoundError, 
    )

def calculate_ability_modifier(score: int) -> int:
    """Fórmula estándar de Pathfinder 2e para modificadores de atributo."""
    return math.floor((score - 10) / 2)

def calculate_proficiency_bonus(level: int, rank: int) -> int:
    """Calcula el bono de competencia: Nivel + (Rango * 2) si Rango > 0."""
    if rank <= 0:
        return 0
    return level + (rank * 2)

def get_name_df(df, name, column = "name", df_name = "DataFrame"):
    """Get Dataframe row by name"""
    row = df[df[column] == name]
    if len(row) > 1:
        raise DataFrameMultipleRowsError(name, column, df_name)
    elif len(row) == 0:
        return []
    return row.iloc[0]
