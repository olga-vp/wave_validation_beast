# wave_validation_beast
Wave model validation scripts


validation.py runs the others and ideally you only have to modify it, except in case of bugs.

You may have to modify the dates in matching.py depending on the format of you dates. I have commented the most probable lines that might cause trouble in the script.

The validation system is arranged to use monthly netcdf files. However, if your files are yearly or cover multiple months, it will work if you name the files by a certain format (for example: BALMFC_201605_FinngrundetWR.nc) that includes the number of the month from which the data starts. The program will read the file until the end and match the times that are available.

You have to create the file structure manually. You can model it after the file paths in validation.py. Note that in the plots folder you must have sub folders named after the variables you're validating. The buoy files should be arranged like this: in 'buoypath' there are separate folders for each buoy, named according to the buoys name in 'buoyfilelist'


validation.py > Runs the other scripts. 



matching.py > Makes matched timeseries of the required variables and saves them in numpy.array format. 

stats.py > Calculates statistics for the individual buoys and quality checks the timeseries. The scripts after this use quality checked arrays produced by this script.

plot.py > Makes box plots for the individual buoys (and scatter plots and timeseries) 

plot_all.py > Makes box plots for all the buoys together (and scatter plots)

stats_all.py > Calculates overall statistics
