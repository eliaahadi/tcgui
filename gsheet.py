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
    def __init__(self, name=None, input_value=0,delay="0ms"):
        self.name = name
        self.input_value = input_value
        self.delay = delay
        self.sheet = ""


    def setup(self):
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
        client = gspread.authorize(creds)

        # sheet1 = client.open("networkstats").sheet1
        self.sheet = client.open("networkstats").get_worksheet(1)
        # logging.debug("sheet info", self.sheet)
        # return self.sheet



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

    def tc_delay_command(self):
        try:
            self.delay
        except TypeError:
            self.delay = '0ms'
        
        result = subprocess.run(["sudo", "tc", "qdisc", "add", "dev", "enp4s0", "root", "netem", "delay", "0ms"],stdout=subprocess.PIPE)
        result = subprocess.run(["sudo", "tc", "qdisc", "change", "dev", "enp4s0", "root", "netem", "delay", self.delay],stdout=subprocess.PIPE)

        # tc_dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        # logging.debug("udp -> %s", dictjson)
        # return tc_dictjson

    def connected(self):
        self.tc_delay_command()
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
                            cell_list_keys = self.sheet.range('B2:F2')
                            cell_list_values = self.sheet.range('B3:F3')

                            for cell, item in zip(cell_list_keys, list(conndict.keys())):
                                cell.value = item
                            self.sheet.update_cells(cell_list_keys)
                            for cell, item in zip(cell_list_values, list(conndict.values())):
                                cell.value = item
                            self.sheet.update_cells(cell_list_values)


    def data_manipulation_tcp(self):
        # iperf3_command()
        # self.connected()
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
                            cell_list_keys = self.sheet.range('B10:F10')
                            cell_list_values = self.sheet.range('B11:F11')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = self.sheet.range('B15:F15')
                            cell_list_values = self.sheet.range('B16:F16')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = self.sheet.range('B20:F20')
                            cell_list_values = self.sheet.range('B21:F21')
                        else:
                            cell_list_keys = self.sheet.range('B5:F5')
                            cell_list_values = self.sheet.range('B6:F6')

                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_keys)

                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_values)

                    if (key == 'sum_received'):
                        logging.debug(list(values.keys()))
                        del values['start']
                        del values['end']
                        # del values['retransmits']
                        if (self.name == 'Rate' and self.input_value == '1M'):
                            cell_list_keys = self.sheet.range('B12:F12')
                            cell_list_values = self.sheet.range('B13:F13')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = self.sheet.range('B17:F17')
                            cell_list_values = self.sheet.range('B18:F18')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = self.sheet.range('B22:F22')
                            cell_list_values = self.sheet.range('B23:F23')
                        else:
                            cell_list_keys = self.sheet.range('B7:F7')
                            cell_list_values = self.sheet.range('B8:F8')


                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_keys)

                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_values)

    def data_manipulation_udp(self):
        for ka, va in self.iperf3_command_udp(cli_args().Value).items():
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
                            cell_list_keys = self.sheet.range('K10:S10')
                            cell_list_values = self.sheet.range('K11:S11')
                        elif (self.name == 'Rate' and self.input_value == '5M'):
                            cell_list_keys = self.sheet.range('K15:S15')
                            cell_list_values = self.sheet.range('K16:S16')
                        elif (self.name == 'Rate' and self.input_value == '10M'):
                            cell_list_keys = self.sheet.range('K20:S20')
                            cell_list_values = self.sheet.range('K21:S21')
                        # elif (self.name == 'Rate' and self.input_value != undefined and self.delay is v) :
                        #     cell_list_keys = self.sheet.range('K20:S20')
                        #     cell_list_values = self.sheet.range('K21:S21')
                        else:
                            cell_list_keys = self.sheet.range('K5:S5')
                            cell_list_values = self.sheet.range('K6:S6')

                        for cell, item in zip(cell_list_keys, list(values.keys())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_keys)

                        # cell_list_values = self.sheet.range('A4:E4')
                        for cell, item in zip(cell_list_values, list(values.values())):
                            cell.value = item
                        self.sheet.update_cells(cell_list_values)

def cli_args():
    parser = argparse.ArgumentParser()
    Name = parser.add_argument("--Name", required=False)
    Value = parser.add_argument('--Value', required=False)
    Delay = parser.add_argument('--Delay', required=False)
    arg_inputs = parser.parse_args() 
    # logging.info("name arg -> %s", arg_inputs.Name)
    # logging.info("Value arg -> %s", arg_inputs.Value)
    return arg_inputs


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # name = parser.add_argument("--Name", required=False)
    # Value = parser.add_argument('--Value', type=int, required=False)
    # arg_inputs = parser.parse_args() 
    # logging.info("name arg -> %s", arg_inputs.Name)
    # cli_args
    # logging.info("name arg -> %s", cli_args().Name)
    # logging.info("Value arg -> %s", cli_args().Value)
    # tcgui_rules()

    if (cli_args().Name and cli_args().Value and cli_args().Delay):
        instanceScript = Iperf3toGoogleSheets(cli_args().Name,cli_args().Value, cli_args().Delay)
    else:
        instanceScript = Iperf3toGoogleSheets()

    # instanceScript = Iperf3toGoogleSheets()
    instanceScript.setup()
    # instanceScript.connected()
    # instanceScript.tc_delay_command(cli_args().Delay)
    instanceScript.data_manipulation_tcp()
    instanceScript.data_manipulation_udp()


# tasks TODO , think how to modularize code better
# break up if/else statements into one function with the inputs mapped to different sheet cells


