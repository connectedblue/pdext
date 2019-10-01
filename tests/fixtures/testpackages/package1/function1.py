from .common import circumference

def calculate_circumference_from_radius(df, radius):
    """
    Calculate the circumference of a circle
    Input:
        df -- dataframe
        radius -- column name containing the radius values
    """
    df['circumference1_from_radius'] = circumference(df[radius])
