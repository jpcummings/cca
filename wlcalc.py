#!/usr/bin/env python

import sys
import numpy as np
import pandas as pd



df = pd.read_excel('SD_Credits_r3.xlsx')

credits=df.loc[:,'Credits']
student_crdeit_hours=df.loc[:,'StudentCreditHours']
schedule_type_workload=df.loc[:,'ScheduleTypeWorkload']

cc = df.loc[:,['Credits','StudentCreditHours','ScheduleTypeWorkload']]