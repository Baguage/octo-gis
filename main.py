# This file is a part of the octo-gis project.
#
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/Baguage/octo-gis
#
# Licensed under the MIT License (MIT);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json

import requests
import subprocess
import time
import argparse

SERVER_URL = "http://comgis1.memphistn.gov/arcgis/rest/services/AGO_MapMemphis/MapMemphis_Parcels/MapServer/0"
# SERVER_URL = "http://arcgis.crc.nd.edu:6080/arcgis/rest/services/Ahab/MapServer/0"

if __name__ == "__main__":
    server_url = SERVER_URL
    parser = argparse.ArgumentParser()
    parser.add_argument("--multi", action="store_true", help="Split server output in multiple geojson files")
    args = parser.parse_args()

    if server_url[-1] == "/":
        server_url = server_url[0:-1]

    print "Connecting to the server " + server_url
    start_time = time.time()
    r = requests.get(server_url + "/query?f=json&returnIdsOnly=true&where=1=1&returnCountOnly=true")
    print "Response time: %s sec" % (time.time() - start_time)
    if "count" not in r.json():
        print "Error: Server did not return number of nodes. Please double-check your URL."
        fp = open("server_response.txt", "wb")
        fp.write(r.content)
        fp.close()
        print "Save server response to server_response.txt file"
        exit(1)

    count = r.json()["count"]
    print "Number of nodes: %s" % count
    print "Loading ObjectIds"
    r = requests.get(server_url + "/query?f=json&returnIdsOnly=true&where=1=1")

    object_ids = r.json()["objectIds"]
    print "Loading data"
    start_time = time.time()
    geojson = None
    for i in range(0, 1+count/100):
        print "Processing ids %s .. %s\r" % (str(i*100), str(i*100+99))
        code = ",".join([str(object_id) for object_id in object_ids[i*100:i*100+99]])
        r = requests.get(server_url + "/query?objectIds=" + code + "&geometryType=esriGeometryEnvelope&spatialRel=esriSpatialRelIntersects&outFields=*&returnGeometry=true&maxAllowableOffset=SR=&returnIdsOnly=false&returnCountOnly=false&returnZ=false&returnM=false&returnDistinctValues=false&returnTrueCurves=false&f=json")

        if geojson is None:
            geojson = r.json()
        else:
            # print geojson
            geojson["features"] = geojson["features"] + r.json()["features"]

        if args.multi and i > 0 and i % 250 == 0:
            # Save every 25000 nodes
            print "Saving geojson file"
            fp = open("output-%s.json" % str(i / 250), "wb")
            json.dump(geojson, fp)
            fp.close()
            geojson = None

    if geojson is not None:
        print "Saving geojson file"
        fp = open("output.json", "wb")
        json.dump(geojson, fp)
        fp.close()

    print "Completed in %s sec" % (time.time() - start_time)
    # print ("Number of nodes: %s" % len(geojson["features"]))
    print "Converting to kml format"
    # for i in range(0, number):
    #     print "Processing file %s" % i
    #     subprocess.call("ogr2ogr -skipfailures -F \"ESRI Shapefile\" output-%s.shp output-%s.kmz.json OGRGeoJSON" % (i,i), shell=True)
    # subprocess.call("ogr2ogr -skipfailures -F \"ESRI Shapefile\" output_.shp _output_.json OGRGeoJSON", shell=True)
    retcode = subprocess.call("ogr2ogr -f KML output.kml output.json")
    # print "Merging shapefiles"
    # for i in range(0, number):
    #     print "Processing file %s" % i
    #     subprocess.call("ogr2ogr -F \"ESRI Shapefile\" output-%s.shp output-%s.kmz.json OGRGeoJSON", shell=True)
    if retcode == 0:
        print "Done, output.kml file has been generated"
    else:
        print "Error running ogr2ogr program, exit code %s" % retcode