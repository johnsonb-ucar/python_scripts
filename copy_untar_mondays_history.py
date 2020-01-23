#!/glade/u/apps/ch/opt/python/3.6.8/gnu/8.3.0/pkg-library/20190627/bin/python
# coding: utf-8

# Copyright University Corporation for Atmospheric Research
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0
# This script must be run on Casper or data-access in order to have access to
# campaign storage. To execute it:
# python copy_untar_mondays_history.py

# IMPORT STANDARD LIBRARIES

# Import python3 print function in case a user runs the script using python2.
from __future__ import print_function
import os
import calendar

# DEFINE PATHS

# History Files
history_path = '/glade/campaign/cisl/dares/Reanalyses/' \
               'f.e21.FHIST_BGC.f09_025.CAM6assim.011/atm/hist/'
history_prefix = 'f.e21.FHIST_BGC.f09_025.CAM6assim.011.cam_allinst.e'
history_suffix = '-00000.tar'

# The preassim history files are saved in 2011-2015 while in 2016 the forecast
# history files are saved. This dictionary allows for the desired filename to
# be modified when given a specific year.
history_dart_stages = {
    '2011': '.preassim.',
    '2012': '.preassim.',
    '2013': '.preassim.',
    '2014': '.preassim.',
    '2015': '.preassim.',
    '2016': '.forecast.'
}

# Scratch
scratch_path = '/glade/scratch/johnsonb/reanalysis_atm_hist/'

# DEFINE LISTS AND DICTIONARIES

# Edit this list to include and omit years from being copied and untarred.
years_in_run = [
    '2011', '2012', '2013', '2014', '2015', '2016'
]

# Edit this list to include and omit months from being copied and untarred.
months_in_year = [
    '01', '02', '03', '04', '05', '06',
    '07', '08', '09', '10', '11', '12'
]

# Initialize a dictionary with years_in_run as the keys and empty lists as the
# values.
desired_dates = {
    '2011': [],
    '2012': [],
    '2013': [],
    '2014': [],
    '2015': [],
    '2016': []
}

# Loop through all valid dates in years_in_run and create a 'mm-dd' string if
# a date falls on a Monday, append this string to desired_dates[elm_year].

# Enumerate is an iterator which returns a tuple consisting of an integer
# index and the element itself. We denote these with prefixes idx for  "index"
# and elm for "element" when using enumerate.
for idx_year, elm_year in enumerate(years_in_run):
    # Loop through months 1 - 12
    # Create integer of this_year for use as an argument to passed to calendar.

    for idx_month, elm_month in enumerate(months_in_year):
        # calendar.monthrange returns a two-element tuple containing the day of
        # week of the first day of the month and the number of days in a month
        # (including leap days). By adding 1 to the second element, we get an
        # upper limit for days in month (e.g. 32 for a 31 day month) to pass to
        # range in a list comprehension.
        lim_month = calendar.monthrange(int(elm_year), int(elm_month))[1]+1

        # Create a list of the days in this month over which to iterate.
        days_in_month = [str(int_date).zfill(2) for int_date in
                         range(1, lim_month)]

        # When enumerating days_in_month we set start=1 so that idx_day starts
        # at 1 and ends at the last day in the month.
        for idx_day, elm_day in enumerate(days_in_month):
            day_of_week = calendar.weekday(int(elm_year), int(elm_month),
                                           int(elm_day))

            # The default behavior of calendar is for the week to start on
            # Monday, so if the day of the week is 0, then it is a Monday.
            if day_of_week == 0:
                # Create a mm-dd string.
                mm_dd_string = elm_month + '-' + elm_day
                # Append it to desired_dates[elm_year].
                desired_dates[elm_year].append(mm_dd_string)

print('Desired dates in each year:', desired_dates)

# Check to see if the files exist
for idx_year, elm_year in enumerate(years_in_run):
    for idx_date, elm_date in enumerate(desired_dates[elm_year]):
        elm_month = elm_date[0:2]
        elm_day = elm_date[3:]

        filename = history_prefix + history_dart_stages[elm_year] + elm_year \
            + '-' + elm_date + history_suffix

        archive_path = history_path + elm_year + '-' + elm_month + '/' \
            + filename

        destination_directory = scratch_path + elm_year + '/'

        if os.path.exists(archive_path):
            print("The archive exists. Begin copying and untarring.")

            # Copy the archive to the destination directory
            command = 'cp ' + archive_path + ' ' + destination_directory
            print(command)
            os.system(command)

            # Extract the files to this directory
            command = 'tar -xvf ' + destination_directory + filename + ' -C ' \
                + destination_directory
            print(command)
            os.system(command)

            # Remove the archive. Give this command the absolute path of the
            # copied archive to be extra careful.
            command = 'rm ' + destination_directory + filename
            print(command)
            os.system(command)
            print('\n')

        else:
            print('Warning: ' + archive_path + ' does not exist.')
            print('\n')
