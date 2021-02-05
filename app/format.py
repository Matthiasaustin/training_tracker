import pandas as pd
from datetime import datetime
import os
import glob
import sys
import re

today = datetime.date(datetime.now())


class formats:
    def __init__(self, workbook, worksheet):
        self.workbook = workbook
        self.worksheet = worksheet

