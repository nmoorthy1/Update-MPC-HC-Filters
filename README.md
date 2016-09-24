# Update MPC-HC Filters

This is used to easily check for updates for your [madVR](http://forum.doom9.org/showthread.php?t=146228) and [LAV Filters](http://forum.doom9.org/showthread.php?t=156191) external filters for [Media Player Classic-Home Cinema](https://nightly.mpc-hc.org/).

## Requirements

Python >= 3.3

## Usage
    >>> update.py


To use this, run update.py and for the first run, it will create a filter_versions file as well as download the most recent versions of madVR and LAV Filters. It then runs the exe automatically to update your LAV Filters and extracts and deletes madVR.zip. You need to move the extracted madVR folder to your current installation location to complete updating madVR. For every subsequent run, make sure the filter_versions file is in the same directory as update.py as it needs this file to check if there are newer versions available.
