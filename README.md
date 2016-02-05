Octogis
=====

Tool for downloading content from ArcGIS Server services in geojson format

# System requirements

Tested on Windows 8 and Python 2.7. Requires requests and GDAL (if you want to covert geojson to KML). 

# Usage example

Edit SERVER_URL in main.py and run

main.py 

or

main.py --multi

# Documentation

Full documenation is not yet available.


# Bugs and requests

If you have found a bug or if you have a request for additional functionality, please use the issue tracker on GitHub.

https://github.com/Baguage/octo-gis/issues

# License

You can use this under MIT licences. See LICENSE.txt file for details.

# Author

Alex Vyushkov, baguage[at]gmail.com

# Useful links

http://comgis1.memphistn.gov/arcgis/rest/services/AGO_MapMemphis/MapMemphis_Parcels/MapServer/0/query

http://arcgis.crc.nd.edu:6080/arcgis/rest/services/Ahab/MapServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry=&geometryType=esriGeometryEnvelope&inSR=&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&f=html

http://arcgis.crc.nd.edu:6080/arcgis/rest/services/Ahab/MapServer/0query?f=json&returnIdsOnly=1&where=1=1

http://comgis1.memphistn.gov/arcgis/rest/services/AGO_MapMemphis/MapMemphis_Parcels/MapServer/0/query?f=json&objectIds=1,2,3&geometryType=esriGeometryEnvelope&returnGeometry=1&returnIdsOnly=0&outFields=*&outSR=4326

http://comgis1.memphistn.gov/arcgis/rest/services/AGO_MapMemphis/MapMemphis_Parcels/MapServer/0

