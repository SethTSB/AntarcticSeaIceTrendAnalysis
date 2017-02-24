## ---------------------------------------------------------------------------
## NSIDCDataGrab.py
##
## Downloads the NSIDC sea ice concentration binary files for processing.
## Data are stored on the National Sea Ice Data Center (NSIDC) ftp site.
##
## Created: Nov 2016 - Feb 2017
## Author: Seth Sykora-Bodie - seth.sykora.bodie@duke.edu (for ENV859)
##      With help and advice from Corrie Curtis, Ginny Crothers and John Fay
## ---------------------------------------------------------------------------

# Section #1 Import modules that will be needed for the analysis

print "Importing Python modules"
import sys, os, urllib, datetime, glob, arcpy

#Get folders  via relative paths
print "Finding relative folder pathways"
print arcpy.AddMessage("Finding relative folder pathways")

scriptFldr = os.path.dirname(sys.argv[0])
rootFldr = os.path.dirname(scriptFldr)
dataFldr = os.path.join(rootFldr,"Data")
scratchFldr = os.path.join(rootFldr, "Scratch")
dailyFldr = os.path.join(dataFldr, "DailySSMIFiles")
if not os.path.exists(dailyFldr): os.mkdir(dailyFldr) #remember to add the new Template.txt header file or it won't know how to build the new tiffs later!
tiffFldr = os.path.join(dataFldr,"TiffFiles")  
if not os.path.exists(tiffFldr): os.mkdir(tiffFldr)
tiffPercentFldr = os.path.join(dataFldr,"TiffPercent")
if not os.path.exists(tiffPercentFldr): os.mkdir(tiffPercentFldr)

print "Successfully: imported sys, os, urllib, datetime, glob, arcpy; found file pathways; and created data new folders."
print arcpy.AddMessage("Successfully: imported sys, os, urllib, datetime, glob, arcpy; found file pathways; and created data new folders.")

# Set links to daily and monthly data sources
dailyURL = 'ftp://sidads.colorado.edu/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/'
    #dailyURL = 'https://daacdata.apps.nsidc.org/pub/DATASETS/nsidc0051_gsfc_nasateam_seaice/final-gsfc/south/daily/'

## ---------------------------------------------------------------------------

# Section #2 Create user input for an annual range

# Build sys.argv to allow user to input the year
inputStart = sys.argv[1]
	#inputStart = 2002				#test year
inputStartYr = int(inputStart)
inputStop = sys.argv[2]
	#inputStop = 2003				#test year
inputStopYr = int(inputStop) + 1

# Compile range
AllYears = range(inputStartYr,inputStopYr)     

# Create else/if statement so that the correct starting day is selected for each year
years01 = [1980, 1981, 1983, 1986, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015]
years02 = [1979, 1982, 1984, 1985, 1987]

#Create start day by year
if inputStartYr in years02:
    inputStartDay = 02
elif inputStartYr in years01: 
    inputStartDay = 01
elif inputStartYr == 1988:
    inputStartDay = 13

#Set sensor type by year
startn07 = datetime.date(1979, 1, 2)
endn07 = datetime.date(1987, 8, 20)
startf08 = datetime.date(1987, 8, 21)
endf08 = datetime.date(1991, 12, 18)
startf11 = datetime.date(1991, 12, 19)
endf11 = datetime.date(1995, 9, 29)
startf13 = datetime.date(1995, 9, 30)
endf13 = datetime.date(2007, 12, 31)
startf17 = datetime.date(2008, 1, 1)
	
## ---------------------------------------------------------------------------

# Section #3 Loop through and download the data from 1979 - 2015

print "Starting to download daily SSMI data from the National Sea and Ice Data Center"
print arcpy.AddMessage("Starting to download daily SSMI data from the National Sea and Ice Data Center")

# Parse dates
d = datetime.date(inputStartYr,01,inputStartDay)       
td = datetime.timedelta(days=1)
nextDay = d                           

# Download files inside a loop
for year in AllYears:
    while nextDay.year == year:
        # Build in a line for exceptions if the https link doesn't exist
        try:
            yr = str(nextDay.year)
            mnth = str(nextDay.month)
            mnth = str(mnth).zfill(2)
            dy = str(nextDay.day)
            dy = str(dy).zfill(2)

            #Build the new date
            date = datetime.date(int(yr), int(mnth), int(dy))

            #Set the sensor type
            if date >= startn07 and date <= endn07:
                sens = 'n07'
            elif date >= startf08 and date <= endf08:
                sens = 'f08'
            elif date >= startf11 and date <= endf11:
                sens = 'f11'
            elif date >= startf13 and date <= endf13:
                sens = 'f13'
            elif date >= startf17:
                sens = 'f17'

            #Build the new url name
            dailyFN = 'nt_' + yr + mnth + dy + '_' + sens + '_v1.1_s.bin'
            NewURL = dailyURL + yr + '/' + dailyFN 

            #Create the output file
            outFN = os.path.join(dailyFldr,dailyFN)
            if os.path.exists(outFN):
                print "-->{} exists; skipping".format(outFN)
                print arcpy.AddMessage("-->{} exists; skipping".format(outFN))
                
            #Write to the local file
            urllib.urlretrieve(NewURL,outFN)
            print "downloading and writing file: " + dailyFN
            print arcpy.AddMessage("downloading and writing file: " + dailyFN)

        # Close out the ftp exceptions error skip
        except Exception:
            pass

        #Add days to create new date URL
        nextDay = nextDay + td

    print "Finished downloading files for " + str(year) 
    print arcpy.AddMessage("Finished downloading files for " + str(year))
    
print "The script has completed downloading the sea ice concentration data from NSIDC, beginning conversion now"
print arcpy.AddMessage("The script has completed downloading the sea ice concentration data from NSIDC, beginning conversion now")

## ---------------------------------------------------------------------------

# Section #4 Loop through filenames to change file extensions from .bin to .bil and shorten filename to create consistent format across all months and years
        # Original file format from NSIDC for reference'nt_YYYYMM_n07_v1.1_n.bin'
        # http://nsidc.org/data/docs/daac/nsidc0051_gsfc_seaice.gd.html

print "Changing file extensions for all files in {}".format(dailyFldr)
print arcpy.AddMessage("Changing file extensions for all of the .bin files")

for filename in glob.iglob(os.path.join(dailyFldr, '*.bin')):
    os.rename(filename, filename[:-15] + '.bil')

print "The script has successfully renamed and changed all file extensions to .bil"
print arcpy.AddMessage("The script has successfully renamed and changed all file extensions to .bil")

## ---------------------------------------------------------------------------

# Section #5 Create matching header text files (the conversion to TIFF requires a text file (.hdr) that gives column and row headers for the new file

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

print "New .txt header files were successfully created for each binary daily NSIDC file"
print arcpy.AddMessage("New text header files were successfully created for each .bil file")

## ---------------------------------------------------------------------------

# Section #6 Convert .bil files to TIFFs

# Set geoprocessing environments
print "Setting geoprocessing environments"
print arcpy.AddMessage("Setting geoprocessing environments")
arcpy.env.scratchWorkspace = scratchFldr
arcpy.env.workspace = dailyFldr
arcpy.env.overwriteOutput = True

print "Beginning to convert binary files into tiff files"
print arcpy.AddMessage("Beginning to convert binary files into tiff files")

# Loop through binary files and convert them
for filename in glob.iglob(os.path.join(dailyFldr, '*.bil')):
    arcpy.RasterToOtherFormat_conversion(filename, tiffFldr, "TIFF")

print "The .tiff output files are almost complete"
print arcpy.AddMessage("The .tiff output files are almost complete")

## ---------------------------------------------------------------------------

# Section #7 Define projection to custom coordinate system created per NSIDC parameters found here:
        # http://nsidc.org/support/21680984-How-do-I-import-the-0051-sea-ice-concentration-data-into-ArcGIS-

print "Defining projection for all files in {}".format(tiffFldr)
print arcpy.AddMessage("Defining the projection for all files")

projectionFile = scriptFldr + "\\Southern_Polar_Projected.prj"
spatialRef = arcpy.SpatialReference(projectionFile)

for filename in glob.iglob(os.path.join(tiffFldr, '*.tif')):
    arcpy.DefineProjection_management(filename, spatialRef)

print "Projection has been defined for all files in {}".format(tiffFldr)
print arcpy.AddMessage("The projection has been defined for all files")

print "Tiff files ready for analysis in ArcMap!"
print arcpy.AddMessage("Tiff files ready for visualization and analysis")

print "Now, in the main root folder, open up the SeaIceData.mxd file, and navigate to \\Data\\TiffFiles."
print arcpy.AddMessage("Now, in the main root folder, open up Data file, and click and drag a .tiff into the map")

## ---------------------------------------------------------------------------

# Section #8 Create rasters without sea ice concentration percentages for each cell

