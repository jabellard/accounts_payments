import os
try:
    from .local import *
except:
    PRODUCTION = 0
    if 'PRODUCTION' in os.environ:
        PRODUCTION = os.environ['PRODUCTION']

    if PRODUCTION:
        from .production import *
    else:
        from .development import *
