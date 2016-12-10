##----------------------------------------------------------------------
## NSIDCDataGrab.py
##
## Downloads the NSIDC sea ice concentration binary files for processing.
## Data are stored on the National Sea Ice Data Center (NSIDC) ftp site.
##
## Created: Nov 2016
## Author: Seth Sykora-Bodie - seth.sykora.bodie@duke.edu (for ENV859)
##      With help and advice from Corrie Curtis, Ginny Crothers and John Fay
##----------------------------------------------------------------------

# Section #1

#Import modules that will be needed for the analysis
print "Importing Python modules"
import sys, os, urllib, datetime, glob, arcpy

#Get folders  via relative paths

print "  "
print "Finding relative folder pathways"

scriptFldr = os.path.dirname(sys.argv[0])
rootFldr = os.path.dirname(scriptFldr)
dataFldr = os.path.join(rootFldr,"Data")
scratchFldr = os.path.join(rootFldr, "Scratch")
dailyFldr = os.path.join(dataFldr, "DailySSMIFiles")
        #if not os.path.exists(dailyFldr): os.mkdir(dailyFldr)
        #remember to add the new Template.txt header file or it won't know how to build the new tiffs later!
tiffFldr = os.path.join(dataFldr,"TiffFiles")  
        #if not os.path.exists(tiffFldr): os.mkdir(tiffFldr)

print "  "
print "Successfully: imported sys, os, urllib, datetime, glob, arcpy; found file pathways; and created data new folders."
print "  "

# Monthly data sources
monthlyURL = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/monthly/'
monthlyFN = 'nt_197811_n07_v1.1_s.bin'     

# Daily data sources
dailyURL = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/'
dailyFN = 'nt_19790102_n07_v1.1_s.bin'

print "Starting to download daily SSMI data from the National Sea and Ice Data Center"

## ---------------------------------------------------------------------------

# Section #1 Loop through and download the data from 1979 - 1980

d = datetime.date(1979,01,02)
td = datetime.timedelta(days=2)
nextDay = d

# Allow the user to input the year               """AllYears = [1979,1980]"""
inputStart = sys.argv[1]
inputStartYr = int(inputStart)
inputStop = sys.argv[2]
inputStopYr = int(inputStop)

AllYears = [inputStartYr,inputStopYr]                            

# Download files inside a loop
for year in AllYears:
    while nextDay.year == year:
        yr = str(nextDay.year)
        mnth = str(nextDay.month)
        mnth = str(mnth).zfill(2)
        dy = str(nextDay.day)
        dy = str(dy).zfill(2)

        #Build the new url name
        dailyFN = 'nt_' + yr + mnth + dy + '_n07_v1.1_s.bin'
        NewURL = dailyURL + yr + '/' + dailyFN 

        #Create the output file
        outFN = os.path.join(dailyFldr,dailyFN)
        if os.path.exists(outFN):
            print "-->{} exists; skipping".format(outFN)

        #Write to the local file
        urllib.urlretrieve(NewURL,outFN)
        print "downloading and writing file: " + dailyFN

        #Add days to create new date URL
        nextDay = nextDay + td

    print "Finished downloading files for " + str(year) 

print "  "
print "The script has completed downloading the sea ice concentration data from NSIDC"

## ---------------------------------------------------------------------------

# Section #2

# Loop through filenames to change file extensions from .bin to .bil
# and shorten filename to create consistent format across all months and years
        # Original file format from NSIDC for reference
        # 'nt_YYYYMM_n07_v1.1_n.bin'
        # http://nsidc.org/data/docs/daac/nsidc0051_gsfc_seaice.gd.html

print "  "
print "Changing file extensions for all files in {}".format(dailyFldr)

for filename in glob.iglob(os.path.join(dailyFldr, '*.bin')):
    os.rename(filename, filename[:-15] + '.bil')

print "The script has uccessfully renamed and changed all file extensions"
print "  "

## ---------------------------------------------------------------------------

# Section #3
# Create matching header text files (the conversion to TIFF requires a 
# text file (.hdr) that gives column and row headers for the new file

headerFile = dailyFldr + "\\template.txt"
for filename in glob.iglob(os.path.join(dailyFldr, '*.bil')):
    def copy(File1, File2): 
        opener1 = open(File2, 'w') 
        opener2 = open(File1, 'r') 
        reader = opener2.read() 
        opener1.write(reader) 
        opener1.close() 
        opener2.close() 
    copy(headerFile, dailyFldr + '\\headerTemplateTwo.txt')    
    newHeader = dailyFldr + '\\headerTemplateTwo.txt'
    os.rename(newHeader, filename[:-4] + '.hdr')

print "  "
print "New .txt header files were successfully created for each binary daily NSIDC file"
print "  "

## ---------------------------------------------------------------------------

# Section #4

# Set geoprocessing environments
print "Setting geoprocessing environments"
arcpy.env.scratchWorkspace = scratchFldr
arcpy.env.workspace = dailyFldr
arcpy.env.overwriteOutput = True

print "  "
print "Beginning to convert binary files into tiff files"
print "  "

# Loop through binary files and convert them

for filename in glob.iglob(os.path.join(dailyFldr, '*.bil')):
    arcpy.RasterToOtherFormat_conversion(filename, tiffFldr, "TIFF")

print "  "
print "The .tiff output files are complete"
print "  "

## ---------------------------------------------------------------------------

# Section #5

# Define projection to custom coordinate system created per NSIDC parameters found here:
# http://nsidc.org/support/21680984-How-do-I-import-the-0051-sea-ice-concentration-data-into-ArcGIS-

print "  "
print "Defining projection for all files in {}".format(tiffFldr)
print "  "

projectionFile = scriptFldr + "\\Southern_Polar_Projected.prj"
spatialRef = arcpy.SpatialReference(projectionFile)

for filename in glob.iglob(os.path.join(tiffFldr, '*.tif')):
    arcpy.DefineProjection_management(filename, spatialRef)
    print "Defining projection for {}".format(filename)

print "  "
print "Projection has been defined for all files in {}".format(tiffFldr)
print "  "
print "Tiff files ready for analysis in ArcMap!"
print "  "
print "Now, in the main root folder, open up the SeaIceData.mxd file, and navigate to \\Data\\TiffFiles."