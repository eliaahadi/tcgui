import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import subprocess
import argparse

import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# use creds to create a client to interact with the Google Drive API



class Iperf3toGoogleSheets:
    def __init__(self, name='None', input_value=0):
        self.name = name
        self.input_value = input_value


    def setup(self):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        sheet1 = client.open("networkstats").sheet1
        sheet2 = client.open("networkstats").get_worksheet(1)
        return sheet2


    def iperf3_command(self):
        result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J"],stdout=subprocess.PIPE)

        dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        return dictjson

    def data_manipulation(self, setup):
        # iperf3_command()
        for ka, va in self.iperf3_command().items():
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
                            # output_conndict_keys = sheet2.insert_row(list(conndict.keys()),1)
                            # output_conndict_values = sheet2.insert_row(list(conndict.values()),2)
                            if (self.name == 'Rate' and self.input_value == 'OneM'):
                                cell_list_keys = setup.range('A1:E1')
                                cell_list_values = setup.range('A2:E2')
                            else:
                                cell_list_keys = setup.range('F1:J1')
                                cell_list_values = setup.range('F2:J2')
                            for cell, item in zip(cell_list_keys, list(conndict.keys())):
                                cell.value = item
                            setup.update_cells(cell_list_keys)

                            # if (name == 'Rate' and input_value == 1):
                            #     cell_list_keys = setup.range('A1:E1')
                            # else:
                            #     cell_list_keys = setup.range('F1:J1')
                            # cell_list_values = setup.range('A2:E2')
                            for cell, item in zip(cell_list_values, list(conndict.values())):
                                cell.value = item
                            setup.update_cells(cell_list_values)
                    
                    if (key == 'sum_sent'):
                        sumsent = values
                        logging.debug(sumsent)
                        # output_sum_sent_keys = sheet2.insert_row(list(values.keys()),3)
                        # output_sum_sent_values = sheet2.insert_row(list(values.values()),4)
                        # cell_list_keys = setup.range('A3:E3')


                        if (self.name == 'Rate' and self.input_value == 'OneM'):
                            cell_list_keys = setup.range('A3:E3')
                            cell_list_values = setup.range('A4:E4')
                        else:
                            cell_list_keys = setup.range('F3:J3')
                            cell_list_values = setup.range('F4:J4')

                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        setup.update_cells(cell_list_keys)

                        # cell_list_values = setup.range('A4:E4')
                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        setup.update_cells(cell_list_values)

                    if (key == 'sum_received'):
                        # output_sum_received_keys = sheet2.insert_row(list(values.keys()),5)
                        # output_sum_received_values = sheet2.insert_row(list(values.values()),6)
                        logging.debug(list(values.keys()))
                        # cell_list_keys = setup.range('A5:E5')

                        if (self.name == 'Rate' and self.input_value == 'OneM'):
                            cell_list_keys = setup.range('A5:E5')
                            cell_list_values = setup.range('A6:E6')
                        else:
                            cell_list_keys = setup.range('F5:J5')
                            cell_list_values = setup.range('F6:J6')


                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        setup.update_cells(cell_list_keys)

                        # cell_list_values = setup.range('A6:E6')
                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        setup.update_cells(cell_list_values)





if __name__ == "__main__":
    # execute only if run as a script
    parser = argparse.ArgumentParser()
    parser.add_argument("--Name", required=False)

    # parser.add_argument("--rate")
    parser.add_argument('--Number', required=False)
    args = parser.parse_args()

    if args.Name:
        instanceScript = Iperf3toGoogleSheets(args.Name,args.Number)
    else:
        instanceScript = Iperf3toGoogleSheets()
    # setupinfo = instanceScript.setup()
    # instanceScript.iperf3_command()
    # instanceScript.data_manipulation(instanceScript.setup(), 'Rate', )
    instanceScript.data_manipulation(instanceScript.setup())



# def myprint(d):
#   for k, v in d.items():
#     if isinstance(v, dict):
#       myprint(v)
#     else:
#       print("{0} : {1}".format(k, v))
# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
# Extract and print all of the values
# list_of_hashes = sheet1.get_all_records()

# row1 = sheet1.row_values(1)

# col1 = sheet1.col_values(1)

# onebyone = sheet1.cell(1, 1).value
# update_onebyone = sheet1.update_cell(2, 1, "I just wrote to a spreadsheet using Python!")
# row = ["I'm","inserting","a","row","into","a,","Spreadsheet","with","Python"]
# index = 25
# rowupdate = sheet1.insert_row(row, index)
# logging.debug(list_of_hashes, row1, col1, onebyone, update_onebyone, sheet1.row_count)
# sheet.delete_row(25)

# sheet1.row_count


# cell_list = sheet1.range('A25:C30')

# for cell in cell_list:
#     cell.value = 'O_o'

# Update in batch
# sheet.update_cells(cell_list)




# subprocess.run(["ls", "-l"])

# subprocess.run(["iperf3", "-c", "192.168.5.166", "-p", "3000", "-t", "30"])


# for value in result:
# logging.debug(result.stdout.decode('utf-8'))   #CompletedProcess instance
# logging.debug(type(result.stdout.decode('utf-8'))) #str
# logging.debug(type(json.JSONDecoder().decode(result.stdout.decode('utf-8')))) #dict


# output_insert = sheet2.insert_row(['tanoshi','hoshi'],1)
