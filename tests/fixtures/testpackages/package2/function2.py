from .common import circumference

def calculate_circumference_from_diameter(df, diameter):
    """
    Calculate the circumference of a circle
    Input:
        df -- dataframe
        radius -- column name containing the diameter values
    """
    df['circumference2_from_diameter'] = circumference(df[diameter]/2)
