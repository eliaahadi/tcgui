import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

def myprint(d):
  for k, v in d.items():
    if isinstance(v, dict):
      myprint(v)
    else:
      print("{0} : {1}".format(k, v))

# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sheet1 = client.open("networkstats").sheet1
sheet2 = client.open("networkstats").get_worksheet(1)

# Extract and print all of the values
list_of_hashes = sheet1.get_all_records()

row1 = sheet1.row_values(1)

col1 = sheet1.col_values(1)

onebyone = sheet1.cell(1, 1).value
update_onebyone = sheet1.update_cell(2, 1, "I just wrote to a spreadsheet using Python!")
row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
index = 25
rowupdate = sheet1.insert_row(row, index)
logging.debug(list_of_hashes, row1, col1, onebyone, update_onebyone, rowupdate, sheet1.row_count)
# sheet.delete_row(25)

sheet1.row_count


cell_list = sheet1.range('A25:C30')

for cell in cell_list:
    cell.value = 'O_o'

# Update in batch
# sheet.update_cells(cell_list)


import subprocess
# subprocess.run(["ls", "-l"])

# subprocess.run(["iperf3", "-c", "192.168.5.166", "-p", "3000", "-t", "30"])
result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J"],stdout=subprocess.PIPE)

import json

# for value in result:
logging.debug(result.stdout.decode('utf-8'))   #CompletedProcess instance
logging.debug(type(result.stdout.decode('utf-8'))) #str
logging.debug(type(json.JSONDecoder().decode(result.stdout.decode('utf-8')))) #dict


dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
# output_insert = sheet2.insert_row(['tanoshi','hoshi'],1)

for ka, va in dictjson.items():
    logging.debug(type(ka)) #str
    logging.debug(type(va)) #dict
    # myprint(va)
    if (isinstance(va, dict)):
        for key,values in va.items():
            logging.debug(type(values)) #string
            logging.debug((key)) #string
            logging.debug((values)) #string
            if (key == 'connected'):
                connectedlist = values
                logging.debug(connectedlist)
                for conndict in values:
                    output_conndict_keys = sheet2.insert_row(list(conndict.keys()),1)
                    output_conndict_values = sheet2.insert_row(list(conndict.values()),2)
            if (key == 'sum_sent'):
                sumsent = values
                logging.debug(sumsent)
                output_sum_sent_keys = sheet2.insert_row(list(values.keys()),3)
                output_sum_sent_values = sheet2.insert_row(list(values.values()),4)
            if (key == 'sum_received'):
                output_sum_received_keys = sheet2.insert_row(list(values.keys()),5)
                output_sum_received_values = sheet2.insert_row(list(values.values()),6)
                # for k,v in values.items():
                #     # sumreceived = k
                #     x = []
                #     y = []
                #     x.extend(k)
                #     logging.debug(list(values.keys()))
                #     logging.debug(v)
                    # output_insert = sheet2.insert_row(list(values.keys()),3)
                    # output_insert2 = sheet2.insert_row(list(v),4)
        # strtodict = json.JSONDecoder().decode(values)
        # for kb, vb in strtodict.items():
        #     logging.debug(kb)
#       for key, string in vb.items():
#           print( '    ' + repr((key, string)))
# for item in list(result.stdout.decode('utf-8')):
    # logging.info(item)
# output_insert2 = sheet2.insert_row(list(result.stdout.decode('utf-8')),2)


