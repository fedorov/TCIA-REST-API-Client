
import urllib2, urllib, string, sys
#
# Refer https://wiki.cancerimagingarchive.net/display/Public/REST+API+Usage+Guide for complete list of API
#
class TCIAClient:
    def __init__(self, apiKey):
        self.apiKey = apiKey
            
        
    def execute(self, baseUrl, queryParameters={}):
        headers = {"api_key" : self.apiKey }
        queryString = "?%s" % urllib.urlencode(queryParameters);
        requestUrl = baseUrl + queryString
        request = urllib2.Request(url=requestUrl , headers=headers)
        resp = urllib2.urlopen(request);
        return resp
                
# Test GetCollectionValues
keyFile = open('/Users/fedorov/tcia_api.key','r')
key = keyFile.readline()[:-1]
print 'Using key \"',key,'\"'
TCIAClient = TCIAClient(key)  # Set the API-Key
# Test GetImages

seriesUID = sys.argv[1]
response = TCIAClient.execute(baseUrl="https://services.cancerimagingarchive.net/services/TCIA/TCIA/query/getImage", queryParameters={ "series_instance_uid" : seriesUID})  # Set baseURL and  queryParams - series_instance_uid

# Save server response as images.zip in current directory
if response.getcode() == 200:
    bytesRead = response.read()
    fout = open("images.zip", "wb")
    fout.write(bytesRead)
    fout.close()
    print "\nDownloaded file images.zip from the server"
else:
    print "Error : " + str(response.getcode) # print error code
