from pdext import *

# Define some standard dataframe content that can
# be used across tests

def A_test_df():
    data = [{'letters': ['a', 'b', 'c']},
            {'numbers': [ 1,   2,   3]}]
    return pd.DataFrame(data)

def X_test_df():
    data = [{'letters': ['x', 'y', 'z']},
            {'numbers': [ 7,   8,   9]}]
    return pd.DataFrame(data)