import concurrent.futures
from simple_salesforce import Salesforce
import requests
import os
import csv
import re
import logging
import argparse

#https://github.com/django/django/blob/main/django/utils/text.py
def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)

def main():

    #Setup logging
    logging.basicConfig(format='INFO: %(message)s', level=logging.getLevelName('INFO'))

    # Setup arguments
    parser = argparse.ArgumentParser(description='Export Attachments from Salesforce')
    parser.add_argument('-q', '--query', metavar='query', required=True, help='SOQL to limit the valid Attachments. Must query the id of the parent record.')
    parser.add_argument('-u', '--username', metavar='uesrname', required=True, help='Username for the org')
    parser.add_argument('-p', '--password', metavar='password', required=True, help='Password for the org')
    parser.add_argument('-t', '--token', metavar='token', required=False, help='Optional token. You can also white list your IP to use this without token')
    parser.add_argument('-s', '--sandbox', metavar='sandbox', required=False, help='Is sandbox? Set to True if you want to connect to test.salesforce.com.')
    args = parser.parse_args()

    # Get arguments from command
    username = args.username
    password =  args.password
    token = args.token

    if not token:
        token = ''

    query = args.query
    is_sandbox = args.sandbox
    if not is_sandbox:
        is_sandbox = False
 
    domain = 'login'
    if is_sandbox == 'True':
        domain = 'test'

    # Initial info logging
    logging.info('Attachments export')
    logging.info('Username: ' + username)
    logging.info('Is Sandbox: ' + str(is_sandbox))
    logging.info('Salesforce Instance: https://'+ domain + '.salesforce.com')

    # Connect To Salesforce
    sf = Salesforce(username=username, password=password, security_token=token, domain=domain)
    logging.info("Successfully connected to Salesforce instance: {0}".format(sf.sf_instance))

    #Build the attachments query
    attachments_query = 'SELECT ID, Body, Name FROM Attachment WHERE ParentID IN ({0})'.format(query)
    attachments_response = sf.query(attachments_query)
    
    #The files will be saved under "Attachments" folder in ths file path
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    output_dir = os.path.join(current_file_path, 'attachments')
    try:
        os.stat(output_dir)
    except:
        os.mkdir(output_dir)

    for attachment in attachments_response["records"]:

        filename = output_dir  + os.sep + attachment["Id"] + "-" + get_valid_filename(attachment["Name"])
        attachment_url = "https://%s%s" % (sf.sf_instance, attachment["Body"])

        logging.info("Downloading Attachment from " + attachment_url)
        response = requests.get(attachment_url, headers={"Authorization": "OAuth " + sf.session_id,"Content-Type": "application/octet-stream"})
        if response.ok:
            # Save file to path
            with open(filename, "wb") as output_file:
                output_file.write(response.content)
            logging.info("Saved file to %s" % filename)
        else:
            logging.info("Something went wrong %s" % attachment_url)
                    
if __name__ == "__main__":
    main()



