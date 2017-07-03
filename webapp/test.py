#!/usr/bin/env python

import os
from utils import fastwebstatics

os.chdir('/usr/local/src/myproject/cdnadmin/webapp/utils')
print fastwebstatics.get_statics_result()
