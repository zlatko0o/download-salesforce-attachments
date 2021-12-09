# Download Attachments Script
Simple python script that allows you to download attachments related to objects

## Getting Started
1. Download the script via raw view or by cloning the repo
2. Install the requirements
```
pip install -r requirements.txt
```

## Usage
```
Export Attachments from Salesforce
  -q query, --query query
                        SOQL to limit the valid Attachments. Must query the id of the parent record.
  -u uesrname, --username uesrname
                        Username for the org
  -p password, --password password
                        Password for the org
  -t token, --token token
                        Optional token. You can also white list your IP to use this without token
  -s sandbox, --sandbox sandbox
                        Is sandbox? Set to True if you want to connect to test.salesforce.com
```

## Example
You can use the script without security token with your IP whitelisted 
```
download.py -q 'SELECT Id FROM Account' -u 'admin@admin.com' -p 'verystrongpassword'
```

If you have security token
```
download.py -q 'SELECT Id FROM Account' -u 'admin@admin.com' -p 'verystrongpassword' -t 'token'
```

If you want to connect to sandbox
```
download.py -q 'SELECT Id FROM Account' -u 'admin@admin.com' -p 'verystrongpassword' -s True
```
