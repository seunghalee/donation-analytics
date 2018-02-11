#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Insight Data Engineering Coding Challenge - Donation Analytics
Created on Sat Feb 10 17:08:47 2018
@author: Seungha Lee
"""

import datetime
import os, sys
import math


def donation_analytics(input_filepath, percentile_filepath, output_file):
    # Input file
    file = open(input_filepath)

    percentile_file = open(percentile_filepath,'r')
    percentile = int(percentile_file.read()) # int
    
    # Output file
    # if repeat_donors.txt already exits, delete it
    if os.path.isfile(output_file):
        os.remove(output_file)
    
    donor_info = dict()
    donor_list = set()
    contributions = dict()
    counts = dict()
    total_amount = dict()
    
    for line in file:
        fields = line.split('|')
        
        # Check if other_ID is empty -- only interested in individual contributions
        if not fields[15]: 
            
            # Only analyze records that are properly formatted
            # 0:CMTE_ID | 7: NAME | 10: ZIP CODE | 13:DATE | 14:AMT | 15:OTHER_ID
            if len(fields[13]) == 8 and len(fields[10]) >= 5 and len(fields[7]) != 0 \
             and len(fields[0]) == 9 and len(fields[14]) != 0:
                
                # format transaction date
                fields[13] = '-'.join([fields[13][:2], fields[13][2:4], fields[13][-4:]])
                fields[13] = datetime.datetime.strptime(fields[13], '%m-%d-%Y')
                
                # only use first 5 digits for zip code
                fields[10] = fields[10][:5]
                
                donor_ID = (fields[7],fields[10])
                
                # Check if donor is a repeat donor
                if donor_ID in donor_list:
                    
                    # Check if donation was made later -- in case data was listed out of order
                    if any(fields[13].year > calendar_year.year for calendar_year in donor_info[donor_ID]):
                        recipient = fields[0]
                        zip_code = fields[10]
                        year = fields[13].year

                        counts[(recipient,zip_code,year)] = counts.get((recipient,zip_code,year),0) + 1
                        total_amount[(recipient,zip_code,year)] = total_amount.get((recipient,zip_code,year),0) + int(fields[14])
                        contributions.setdefault((recipient,zip_code,year),[])
                        contributions[(recipient,zip_code,year)].append(fields[14])
                        
                        # Compute running percentile of contributions
                        n = int(math.ceil(percentile/100 * counts[(recipient,zip_code,year)])) # ordinal rank
                        percentile_value = round(float((contributions[(recipient,zip_code,year)][n-1])))
                        
                        output = [recipient,  # CMTE_ID
                                  zip_code,  # 5-digit zip code
                                  year,  # year of contribution
                                  percentile_value,  # running percentile of contributions
                                  total_amount[(recipient,zip_code,year)],  # total amt received
                                  counts[(recipient,zip_code,year)]]  # total number of transactions

                        # Write calculated fields out onto a pipe-delimited line
                        output = '|'.join(map(str,output)) + '\n'
                        
                        with open(output_file,'a') as outfile:
                            outfile.write(output)
    
                donor_info.setdefault(donor_ID,[])
                donor_info[donor_ID].append(fields[13])
                donor_list.add(donor_ID)


if __name__ == "__main__":
    input_filepath = str(sys.argv[1])
    percentile_filepath = str(sys.argv[2])
    output_file = str(sys.argv[3])
    donation_analytics(input_filepath, percentile_filepath, output_file)