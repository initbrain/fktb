# -*- coding: utf-8 -*-

import os
import inspect
import fktb

FKTB_PATH = os.path.dirname(inspect.getfile(fktb))
CONFIG_PATH = os.path.join(os.path.expanduser('~'), '.fktb')