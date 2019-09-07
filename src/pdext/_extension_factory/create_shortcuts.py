

import pandas as pd

def create_shortcuts(shortcuts):
    # each item in shortcuts is in the form <namespace>.<function>
    # The shortcut will be:
    #      pd.<function> = pd.DataFrame().<namespace>.<function>
    for sc in shortcuts:
        ns, fn = sc.split('.')
        ns = getattr(pd.DataFrame(), ns)
        setattr(pd, fn, getattr(ns, fn))
    

    