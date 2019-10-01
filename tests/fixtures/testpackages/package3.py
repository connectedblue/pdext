from math import pi

# module constant defined
tau = 2* pi

# A utility function used by the extensions
def circumference(radius):
    return tau*radius

def calculate_circumference_from_radius(df, radius):
    """
    Calculate the circumference of a circle
    Input:
        df -- dataframe
        radius -- column name containing the radius values
    """
    df['circumference3_from_radius'] = circumference(df[radius])

def calculate_circumference_from_diameter(df, diameter):
    """
    Calculate the circumference of a circle
    Input:
        df -- dataframe
        radius -- column name containing the diameter values
    """
    df['circumference3_from_diameter'] = circumference(df[diameter]/2)