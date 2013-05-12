
import urllib2, urllib, string
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
response = TCIAClient.execute(baseUrl="https://services.cancerimagingarchive.net/services/TCIA/TCIA/query/getCollectionValues", queryParameters={ "modality" : "MR"})  # Set baseURL and queryParams - Modality = MR


if response.getcode() == 200:
    print "Server Returned:\n"
    responseStr = response.read()[:-1]
    print responseStr
    # print response.read()
    
else:
    print "Error : " + str(response.getcode) # print error code

collections = string.split(responseStr,'\n')
print 'Collections:',collections
for c in collections:
  print 'Collection: ',c

  response = TCIAClient.execute(baseUrl="https://services.cancerimagingarchive.net/services/TCIA/TCIA/query/getPatientStudy", queryParameters={ "collection" : c[1:-1]})  # Set baseURL and  queryParams - series_instance_uid
  if response.getcode() == 200:
    print 'Response:',response.read()
  else:
    print "Bad return code"

# Test GetImages

response = TCIAClient.execute(baseUrl="https://services.cancerimagingarchive.net/services/TCIA/TCIA/query/getImage", queryParameters={ "series_instance_uid" : "1.3.6.1.4.1.9328.50.45.305379731379418833489008183081988213374"})  # Set baseURL and  queryParams - series_instance_uid

# Save server response as images.zip in current directory
if response.getcode() == 200:
    bytesRead = response.read()
    fout = open("images.zip", "wb")
    fout.write(bytesRead)
    fout.close()
    print "\nDownloaded file images.zip from the server"
else:
    print "Error : " + str(response.getcode) # print error code
