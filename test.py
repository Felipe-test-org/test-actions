import http.client
import json
import pandas as pd


# Define Global Variables for the Cloud One Workload Security
service = "workload"
region = "us-1"
apikey = "ApiKey 1yS6mV3TFFedyhT3naflfgIVxVM"

# Define Header Variables for the API Calls
apiversion = "v1"
apicall = http.client.HTTPSConnection(service+"."+region+".cloudone.trendmicro.com")

headers = { 'Authorization': apikey, 'api-version': apiversion, 'content-type': "application/json" }

# Open/Read the csv file
csvfile = open('data.csv')
readcsv = pd.read_csv(csvfile)

# Collect data from CSV
ips = readcsv.IP
policy = readcsv.POLICY
relays = readcsv.RELAY
group = readcsv.GROUP
subgroup1 = readcsv.SUBGROUP1
subgroup2 = readcsv.SUBGROUP2
system_os = readcsv.OS

# Counting the size of the arrays
groupsize = len(group)


print('\n - Adding ' + str(groupsize*3) + ' Groups to Workload Security...\n')

# Index for the Groups ID
rootgroupindex = dict()
subgroup1index = dict()

# Add Root Groups
i = 0
while i < groupsize:
  payload = '{\"name\":'+"\""+group[i]+"\""+'}'
  apicall.request("POST", "/api/computergroups",payload, headers)
  res = apicall.getresponse()
  data = json.loads(res.read())
  json_data = json.dumps(data, indent=2)
  print(json_data)
  
  # Query Root Group ID
  payload = '{\"maxItems\":\"1\",\"searchCriteria\":[{\"fieldName\":\"name\",\"stringValue\":'+"\""+group[i]+"\""+'}],\"sortByObjectID\":\"true\"}'
  apicall.request("POST", "/api/computergroups/search",payload, headers)
  res = apicall.getresponse()
  data = json.loads(res.read())
  rootgroupindex[data["computerGroups"][0]['name']] = data["computerGroups"][0]['ID']

  # Add First Sub-Groups
  currentparentid = str(rootgroupindex[group[i]])
  payload = '{\"name\":'+"\""+subgroup1[i]+"\""+', \"parentGroupID\":'+"\""+currentparentid+"\""+'}'
  apicall.request("POST", "/api/computergroups",payload, headers)
  res = apicall.getresponse()
  data = json.loads(res.read())
  json_data = json.dumps(data, indent=2)
  print(json_data)

  # Query Sub-Group1 ID
  payload = '{\"maxItems\":\"1\",\"searchCriteria\":[{\"fieldName\":\"name\",\"stringValue\":'+"\""+subgroup1[i]+"\""+'},{\"fieldName\":\"parentGroupID\",\"numericValue\":'+"\""+currentparentid+"\""+'}],\"sortByObjectID\":\"true\"}'
  apicall.request("POST", "/api/computergroups/search",payload, headers)
  res = apicall.getresponse()
  data = json.loads(res.read())
  subgroup1index[data["computerGroups"][0]['name']] = data["computerGroups"][0]['ID']

  # Add Second Sub-Groups
  currentparentid = str(subgroup1index[subgroup1[i]])
  payload = '{\"name\":'+"\""+subgroup2[i]+"\""+', \"parentGroupID\":'+"\""+currentparentid+"\""+'}'
  apicall.request("POST", "/api/computergroups",payload, headers)
  res = apicall.getresponse()
  data = json.loads(res.read())
  json_data = json.dumps(data, indent=2)
  print(json_data)
  i+=1

# Close the file
csvfile.close()
