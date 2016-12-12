# AntarcticSeaIceTrendAnalysis

Antarctic Sea Ice Concentration Data Download & Conversion Tool

Tool Overview

This Python script and ArcGIS tool contained within this zip file provide the user with a quick and 
easy way to download sea ice concentration data from the National Sea and Ice Data Center (NSIDC) 
website for use in further geospatial analyses as .tiff files. Because the Special Sensor 
Microwave/Imager (SSMI) passive microwave data is provided by NSIDC in binary format, and without any 
spatial reference, numerous steps are required to transform it into a usable format. Steps involved in 
this process of developing the spatially referenced .tiffs include:

1) The script must first access the data repository on the NSIDC website;
2) It must then write these files out into a new directory;
3) It must change their names and extensions prior to conversion with ArcPy;
4) It must sequentially build a new text file for each binary data file with column and row headers 
information;
5) It must then use the binary data file and header file to convert the data into a raster (.tiff);
6) Finally it must provide a unique spatial reference for the data according to the instructions provided 
on the NSIDC website.

Once converted, these spatially referenced raster files can be visualized in ArcMap, or used for further 
analyses. Although not included in this zip file (because the entire library of NSIDC’s entire library of 
NASA images contains 11,000 files!), the complete scripts provide the option for the user to select a 
longer time series (anytime between 1979 and 2015) for download and conversion.

Next Steps

Eventually, this analysis toolkit will include the development of a script to output time series trends 
for user identified study areas or sentinel sites throughout the Antarctic. Eventually, the user will be 
able to open a .mxd file in ArcMap, digitize in a new polygon or select a particular point, this will then 
be converted to a raster file, and underlying cells (imagine a 3-D box, or a Rubik’s cube) in all raster 
files within the selected time frame will be averaged to provide graphs of sea ice concentrations over time.

Data Information

Sea Ice Concentration Data: Additional information non data included in this package is located in the ‘Docs’ 
folder and contains links to websites with data summaries, libraries, and user guides. Remotely sensed data 
for this particular dataset is in 25k km x 25km pixels and covers the entire Antarctic continent. Additional 
shapefiles are included in the data folder for reference use.