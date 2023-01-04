#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 30 15:27:06 2022

@author: dan
"""

import re
import pandas as pd
import numpy as np

# Pattern to search for for deaths in the US only
init_pattern = re.compile(r'USA\s+Dead')

# Pattern to extract age
pattern = re.compile(r'\s*(\D+)\s*\((\d+)\)')

# Search for words implying that the person is no longer an active athlete
former_words = ['ex-', 'former', 'coach', 'teacher']

# Load in lines as text
with open('gs_text.txt', 'rt', encoding='latin1') as fid:
    lines = fid.readlines()
    
# Loop through lines
rows = []
count = 0
n_us = 0
while count < len(lines):
    
    # Check if it references a USA death
    usa = (init_pattern.search(lines[count]) is not None)
        
    count += 1
    
    if usa:
        n_us += 1
        
        # Extract age
        match = pattern.match(lines[count])
        if match is not None:
            
            line_lower = lines[count].lower()
            name = match.group(1).strip()
            age = int(match.group(2))
            former = any([word in line_lower for word in former_words])

            row = (name, age, former)
            rows.append(row)
            
# Collect in data frame
df = pd.DataFrame(rows, columns=['name', 'age', 'former'])

# Count and report results
print("Number of US deaths: {0:d} total, {1:d} per year".format(n_us, int(np.ceil(n_us / 2))))

n_us_age = np.sum(df['age'] <= 39)
print("Number of US deaths < 40 years old: {0:d} total, {1:d} per year".format(n_us_age, int(np.ceil(n_us_age / 2))))

n_us_age_current = np.sum((df['age'] <= 39) & (~df['former']))
print("Number of US deaths < 40 years old, not ex athletes or coaches: {0:d} total, {1:d} per year".format(n_us_age_current, int(np.round(n_us_age_current / 2))))