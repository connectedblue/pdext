from .register_extensions import *
import pandas as pd
import numpy as np

# Set the current version number
from ._version import get_versions
v = get_versions()
__version__ = v.get("closest-tag", v["version"])
__git_version__ = v.get("full-revisionid")
del get_versions, v
