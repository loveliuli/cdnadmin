#!/usr/bin/env python

import os
from utils import fastwebstatics
from webapp.models import Charge_info

os.chdir('/usr/local/src/myproject/cdnadmin/webapp/utils')
print fastwebstatics.get_statics_result()
