import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import subprocess
import argparse
# from main import get_active_rules
import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)


# def tcgui_rules(self):
#     logging.debug("tcgui rules -> %s ", get_active_rules)

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


    def iperf3_command_tcp(self):
        result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J"],stdout=subprocess.PIPE)

        dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        # logging.debug("TCP -> %s", dictjson)
        return dictjson


    def iperf3_command_udp(self, bandwidth_rate):
        try:
            bandwidth_rate
        except TypeError:
            bandwidth_rate = '1M'
        # if (!bandwidth_rate):
        #     bandwidth_rate = '1M'
        result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J", "-u", "-b", bandwidth_rate],stdout=subprocess.PIPE)

        dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        # logging.debug("udp -> %s", dictjson)
        return dictjson


    def connected(self, setup):
        for ka, va in self.iperf3_command_tcp().items():
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
                            cell_list_keys = setup.range('B2:F2')
                            cell_list_values = setup.range('B3:F3')

                            for cell, item in zip(cell_list_keys, list(conndict.keys())):
                                cell.value = item
                            setup.update_cells(cell_list_keys)
                            for cell, item in zip(cell_list_values, list(conndict.values())):
                                cell.value = item
                            setup.update_cells(cell_list_values)


    def data_manipulation_tcp(self, setup):
        # iperf3_command()
        for ka, va in self.iperf3_command_tcp().items():
            logging.debug(type(ka)) #str
            logging.debug(type(va)) #dict
            # myprint(va)
            if (isinstance(va, dict)):
                for key,values in va.items():
                    logging.debug(type(values)) #string
                    logging.debug((key)) #string
                    logging.debug((values)) #string

                    if (key == 'sum_sent'):
                        sumsent = values
                        del values['start']
                        del values['end']
                        del values['retransmits']
                        logging.debug(values)

                        if (self.name == 'Rate' and self.input_value == '1M'):
                            cell_list_keys = setup.range('B10:F10')
                            cell_list_values = setup.range('B11:F11')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = setup.range('B15:F15')
                            cell_list_values = setup.range('B16:F16')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = setup.range('B20:F20')
                            cell_list_values = setup.range('B21:F21')
                        else:
                            cell_list_keys = setup.range('B5:F5')
                            cell_list_values = setup.range('B6:F6')

                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        setup.update_cells(cell_list_keys)

                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        setup.update_cells(cell_list_values)

                    if (key == 'sum_received'):
                        logging.debug(list(values.keys()))
                        del values['start']
                        del values['end']
                        # del values['retransmits']
                        if (self.name == 'Rate' and self.input_value == '1M'):
                            cell_list_keys = setup.range('B12:F12')
                            cell_list_values = setup.range('B13:F13')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = setup.range('B17:F17')
                            cell_list_values = setup.range('B18:F18')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = setup.range('B22:F22')
                            cell_list_values = setup.range('B23:F23')
                        else:
                            cell_list_keys = setup.range('B7:F7')
                            cell_list_values = setup.range('B8:F8')


                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        setup.update_cells(cell_list_keys)

                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        setup.update_cells(cell_list_values)

    def data_manipulation_udp(self, setup):
        for ka, va in self.iperf3_command_udp(cli_args().New_Value).items():
            logging.debug(type(ka)) #str
            logging.debug(type(va)) #dict
            # myprint(va)
            if (isinstance(va, dict)):
                for key,values in va.items():
                    logging.debug(type(values)) #string
                    logging.debug((key)) #string
                    logging.debug((values)) #string
                    if (key == 'sum'):
                        sumsent = values
                        logging.debug(sumsent)
                        del values['start']
                        del values['end']
                        # del values['seconds']
                        del values['jitter_ms']
                        del values['lost_packets']
                        del values['packets']
                        del values['lost_percent']
                        if (self.name == 'Rate' and self.input_value == '1M'):
                            cell_list_keys = setup.range('K10:S10')
                            cell_list_values = setup.range('K11:S11')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = setup.range('K15:S15')
                            cell_list_values = setup.range('K16:S16')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = setup.range('K20:S20')
                            cell_list_values = setup.range('K21:S21')
                        else:
                            cell_list_keys = setup.range('K5:S5')
                            cell_list_values = setup.range('K6:S6')

                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        setup.update_cells(cell_list_keys)

                        # cell_list_values = setup.range('A4:E4')
                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        setup.update_cells(cell_list_values)

def cli_args():
    parser = argparse.ArgumentParser()
    name = parser.add_argument("--Name", required=False)
    new_value = parser.add_argument('--New_Value', required=False)
    arg_inputs = parser.parse_args() 
    # logging.info("name arg -> %s", arg_inputs.Name)
    # logging.info("new_value arg -> %s", arg_inputs.New_Value)
    return arg_inputs


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # name = parser.add_argument("--Name", required=False)
    # new_value = parser.add_argument('--New_Value', type=int, required=False)
    # arg_inputs = parser.parse_args() 
    # logging.info("name arg -> %s", arg_inputs.Name)
    # cli_args
    # logging.info("name arg -> %s", cli_args().Name)
    # logging.info("new_value arg -> %s", cli_args().New_Value)
    # tcgui_rules()

    if (cli_args().Name and cli_args().New_Value):
        instanceScript = Iperf3toGoogleSheets(cli_args().Name,cli_args().New_Value)
    else:
        instanceScript = Iperf3toGoogleSheets()

    # instanceScript = Iperf3toGoogleSheets()
    instanceScript.connected(instanceScript.setup())
    instanceScript.data_manipulation_tcp(instanceScript.setup())
    instanceScript.data_manipulation_udp(instanceScript.setup())


# tasks TODO , think how to modularize code better
# break up if/else statements into one function with the inputs mapped to different sheet cells


