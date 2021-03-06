import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import subprocess
import argparse
# from main import get_active_rules
import logging
import logging.config

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# Log.Logger.setLevel(50,'CRITICAL')
# level = Log.getLevelName('CRITICAL')

Log = logging.getLogger('logger_root')
Log.setLevel('CRITICAL')
# def tcgui_rules(self):
#     Log.debug("tcgui rules -> %s ", get_active_rules)

class Iperf3toGoogleSheets:
    def __init__(self, name=None, input_value="1M",delay="0ms"):
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
        # Log.debug("sheet info", self.sheet)
        # return self.sheet



    def iperf3_command_tcp(self, bandwidth_rate):
        # try:
        #     bandwidth_rate
        # except TypeError:
        #     bandwidth_rate = '1000M'

        try:
            tested_bandwidth_rate = float(bandwidth_rate[:-2])
            tested_bandwidth_rate = str(bandwidth_rate)
        except ValueError:
            tested_bandwidth_rate = '1000MB'
        result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J", "-b", tested_bandwidth_rate],stdout=subprocess.PIPE)

        dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        # Log.debug("TCP -> %s", dictjson)
        return dictjson


    def iperf3_command_udp(self, bandwidth_rate):
        # try:
        #     bandwidth_rate
        # except TypeError:
        #     bandwidth_rate = '1MB'

        try:
            tested_bandwidth_rate = float(bandwidth_rate[:-2])
            tested_bandwidth_rate = str(bandwidth_rate)
            # self.sheet.update_acell('E19', float(cli_args().Value[:-2]))
        except ValueError:
            tested_bandwidth_rate = '1MB'

        # if (!bandwidth_rate):
        #     bandwidth_rate = '1M'
        result = subprocess.run(["iperf3", "-c", "192.168.5.166", "-t", "3", "-J", "-u", "-b", tested_bandwidth_rate],stdout=subprocess.PIPE)

        dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        Log.info("udp -> %s", bandwidth_rate)
        # Log.info("udp 2-> %s", bandwidth_rate)
        return dictjson

    def tc_delay_command(self):
        # try:
        #     self.delay
        # except TypeError:
        #     self.delay = '0ms'
        
        try:
            tested_delay = float(self.delay[:-2])
            tested_delay = self.delay
        except ValueError:
            tested_delay = '0ms'
        Log.debug("BEFORE delay -> %s", self.delay)

        result = subprocess.run(["sudo", "tc", "qdisc", "add", "dev", "enp4s0", "root", "netem", "delay", "0ms"],stdout=subprocess.PIPE)
        result = subprocess.run(["sudo", "tc", "qdisc", "change", "dev", "enp4s0", "root", "netem", "delay", tested_delay],stdout=subprocess.PIPE)

        # tc_dictjson = json.JSONDecoder().decode(result.stdout.decode('utf-8'))
        Log.debug("result -> %s", result)
        # return tc_dictjson

    def data_manipulation_tcp(self):
        # iperf3_command()
        # self.connected()
        # self.tc_delay_command()
        columndict = {'C':'1MB', 'D':'10MB', 'E':'50MB', 'F':'100MB', 'G':'1000MB'}
        columnlist = ['C', 'D', 'E', 'F', 'G', 'H']

        
        # del values['retransmits']
        # if delay = i starting from 0, then cell sheet range is i*10 + 6
        ratelist = ['1MB', '10MB', '50MB', '100MB', '1000MB']
        
        delaylist = []
        for i in range(0, 1100, 100):
            delaylist.append((str(i))+'ms')
        Log.info(delaylist)
        if (self.delay == '0ms'):
            # for i in range
            increment_delay = '6'
        else:
            Log.info("delay variable -> %s", delaylist.__contains__(self.delay))
            # for k in delaylist:
            #     if (int(k))
            if(delaylist.__contains__(self.delay)):
                increment_delay = str(int(self.delay[:-4]) + 6)
            else:
                increment_delay = '17'
            Log.info("TCP increment variable -> %s", increment_delay)
        if (self.name == 'Rate' and self.input_value == 'NA'):
            for letter in columnlist:
                Log.info("letter value -> %s", letter)
                for i in ratelist:
                    Log.info(((i[:-2]))) #<class 'str'>
                    # Log.debug(type(cli_args().Value))
                    for columnkey, columnvalue in columndict.items():
                        if(columnkey == letter and columnvalue == i):
                            for ka, va in self.iperf3_command_tcp(i).items():
                                if (isinstance(va, dict)):
                                    for key,values in va.items():
                                        if (key == 'sum_received'):
                                            bps = values['bits_per_second']
                                            # Log.debug("delay value -> %s", increment_delay)
                                            range_adder = letter + increment_delay + ':' + letter +  increment_delay
                                            cell_list_values = self.sheet.range(range_adder)
                                            Log.debug("cell_list_values -> %s", cell_list_values)
                                            for cell, item in zip(cell_list_values, list(values.values())):
                                                #values.values() 'bits_per_second':77222
                                                cell.value = values['bits_per_second']
                                                Log.debug("cell values -> %s", item)
                                            self.sheet.update_cells(cell_list_values)
        else:
            for ka, va in self.iperf3_command_tcp(cli_args().Value).items():
                Log.info((cli_args().Value)) #str
                Log.info(type(va)) #dict
                # myprint(va)
                if (isinstance(va, dict)):
                    for key,values in va.items():
                        Log.info(type(values)) #string
                        Log.info((key)) #string
                        Log.info((values)) #string

                        if (key == 'connected'):
                            connectedlist = values
                            Log.info(connectedlist)
                            for conndict in values:
                                cell_list_keys = self.sheet.range('B2:F2')
                                cell_list_values = self.sheet.range('B3:F3')

                                for cell, item in zip(cell_list_keys, list(conndict.keys())):
                                    cell.value = item
                                self.sheet.update_cells(cell_list_keys)
                                for cell, item in zip(cell_list_values, list(conndict.values())):
                                    cell.value = item
                                self.sheet.update_cells(cell_list_values)

                        if (key == 'sum_received'):
                            Log.info(list(values.keys()))
                            Log.info(values['bits_per_second'])
                            del values['start']
                            del values['end']
                            bps = values['bits_per_second']
                            # if (self.delay == '0ms'):
                            #     # for i in range
                            #     increment_delay = '6'
                            # else:
                            #     # Log.debug("delay variable -> %s", (int(self.delay[:-4])))
                            #     increment_delay = str(int(self.delay[:-4]) + 6)
                            
                            if (self.name == 'Rate' and self.input_value == '1MB'):
                                range_adder = 'C' + increment_delay + ':C' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '10MB'):
                                range_adder = 'D' + increment_delay + ':D' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '50MB'):
                                range_adder = 'E' + increment_delay + ':E' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '100MB'):
                                range_adder = 'F' + increment_delay + ':F' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '1000MB'):
                                range_adder = 'G' + increment_delay + ':G' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            else:
                                range_adder = 'H' + increment_delay + ':H' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)

                            Log.debug("BPS values -> %s", bps)
                            if (self.input_value != 'NA'):
                                for cell, item in zip(cell_list_values, list(values.values())):
                                    #values.values() 'bits_per_second':1081110.0
                                    cell.value = bps
                                    Log.debug("cell values -> %s", item)
                                self.sheet.update_cells(cell_list_values)

    def data_manipulation_udp(self):

        # self.tc_delay_command()
        columndict = {'I':'1MB', 'J':'10MB', 'K':'50MB', 'L':'100MB', 'M':'1000MB'}
        columnlist = ['I', 'J', 'K', 'L', 'M', 'N']
        ratelist = ['1MB', '10MB', '50MB', '100MB', '1000MB']
        
        delaylist = []
        for i in range(0, 1100, 100):
            delaylist.append((str(i))+'ms')
        Log.info(delaylist)
        if (self.delay == '0ms'):
            increment_delay = '6'
        else:
            if(delaylist.__contains__(self.delay)):
                increment_delay = str(int(self.delay[:-4]) + 6)
            else:
                increment_delay = '17'
            # increment_delay = str(int(self.delay[:-4]) + 6)
            Log.info("UDP increment variable -> %s", increment_delay)
        if (self.name == 'Rate' and self.input_value == 'NA'):
            for letter in columnlist:
                Log.info("letter value -> %s", letter)
                for i in ratelist:
                    Log.debug(((i[:-2]))) #<class 'str'>
                    # Log.debug(type(cli_args().Value))
                    for columnkey, columnvalue in columndict.items():
                        if(columnkey == letter and columnvalue == i):
                            for ka, va in self.iperf3_command_udp(i).items():
                                if (isinstance(va, dict)):
                                    for key,values in va.items():
                                        if (key == 'sum'):
                                            bps = values['bits_per_second']
                                            del values['start']
                                            del values['end']
                                            # del values['seconds']
                                            del values['jitter_ms']
                                            del values['lost_packets']
                                            del values['packets']
                                            del values['lost_percent']
                                            # Log.debug("delay value -> %s", increment_delay)
                                            range_adder = letter + increment_delay + ':' + letter +  increment_delay
                                            cell_list_values = self.sheet.range(range_adder)
                                            Log.debug("cell_list_values -> %s", cell_list_values)
                                            for cell, item in zip(cell_list_values, list(values.values())):
                                                #values.values() 'bits_per_second':77222
                                                cell.value = values['bits_per_second']
                                                Log.debug("cell values -> %s", item)
                                            self.sheet.update_cells(cell_list_values)
        else:
            for ka, va in self.iperf3_command_udp(cli_args().Value).items():
                Log.info(type(ka)) #str
                Log.info(type(va)) #dict
                # myprint(va)
                if (isinstance(va, dict)):
                    for key,values in va.items():
                        Log.info(type(values)) #string
                        Log.info((key)) #string
                        Log.info((values)) #string
                        if (key == 'sum'):
                            sumsent = values
                            Log.info(sumsent['bits_per_second'])
                            del values['start']
                            del values['end']
                            # del values['seconds']
                            del values['jitter_ms']
                            del values['lost_packets']
                            del values['packets']
                            del values['lost_percent']
                            if (self.name == 'Rate' and self.input_value == '1MB'):
                                range_adder = 'I' + increment_delay + ':I' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '10MB'):
                                range_adder = 'J' + increment_delay + ':J' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '50MB'):
                                range_adder = 'K' + increment_delay + ':K' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '100MB'):
                                range_adder = 'L' + increment_delay + ':L' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            elif (self.name == 'Rate' and self.input_value == '1000MB'):
                                range_adder = 'M' + increment_delay + ':M' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)
                            else:
                                range_adder = 'N' + increment_delay + ':N' +  increment_delay
                                cell_list_values = self.sheet.range(range_adder)

                            for cell, item in zip(cell_list_values, list(values.values())):
                                cell.value = sumsent['bits_per_second']
                            self.sheet.update_cells(cell_list_values)
                            if (self.delay not in delaylist and cli_args().Value not in ratelist):
                                Log.info("rate value -> %s", cli_args().Value)
                                Log.info("delay values -> %s", self.delay)
                                Log.info("cell_list values -> %s",cell_list_values)
                                # self.sheet.update_cells('B20', 'test')
                                # self.sheet.update_acell('B23', 'Bingo!')
                                # if 
                                try:
                                    input_rate = float(cli_args().Value[:-2])
                                    self.sheet.update_acell('E19', float(cli_args().Value[:-2]))
                                except ValueError:
                                    self.sheet.update_acell('E19', '1MB')

                                try:
                                    input_delay = float(self.delay[:-2])
                                    self.sheet.update_acell('G19', float(self.delay[:-2]))
                                except ValueError:
                                    self.sheet.update_acell('G19', '0ms')
                            
                            elif (self.delay not in delaylist or cli_args().Value in ratelist):
                                Log.info("rate value -> %s", cli_args().Value)
                                Log.info("delay values -> %s", self.delay)
                                Log.info("cell_list values -> %s",cell_list_values)
                                # self.sheet.update_cells('B20', 'test')
                                # self.sheet.update_acell('B23', 'Bingo!')
                                # self.sheet.update_acell('B19', str(cli_args().Value))
                                try:
                                    input_delay = float(self.delay[:-2])
                                    self.sheet.update_acell('B17', float(self.delay[:-2]))
                                except ValueError:
                                # if ((float(cli_args().Value[:-2])) is not float):
                                # else:
                                    self.sheet.update_acell('B17', '0ms')
                                    # self.sheet.update_acell('N5', 'unlimited')



                                
                            elif (self.delay in delaylist or cli_args().Value not in ratelist):
                                Log.info("rate value -> %s", (cli_args().Value[:-2]))
                                Log.info("delay values -> %s", self.delay)
                                Log.info("cell_list values -> %s",cell_list_values)
                                # self.sheet.update_cells('B20', 'test')
                                # self.sheet.update_acell('B23', 'Bingo!')
                                try:
                                    input_rate = float(cli_args().Value[:-2])
                                    self.sheet.update_acell('H5', input_rate)
                                    self.sheet.update_acell('N5', input_rate)
                                except ValueError:
                                # if ((float(cli_args().Value[:-2])) is not float):
                                # else:
                                    self.sheet.update_acell('H5', '1MB')
                                    self.sheet.update_acell('N5', 'unlimited')
                                # self.sheet.update_acell('B17', str(self.delay))



def cli_args():
    parser = argparse.ArgumentParser()
    Name = parser.add_argument("--Name", required=False)
    Value = parser.add_argument('--Value', required=False)
    Delay = parser.add_argument('--Delay', required=False)
    arg_inputs = parser.parse_args() 
    # Log.info("name arg -> %s", arg_inputs.Name)
    # Log.info("Value arg -> %s", arg_inputs.Value)
    return arg_inputs


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # name = parser.add_argument("--Name", required=False)
    # Value = parser.add_argument('--Value', type=int, required=False)
    # arg_inputs = parser.parse_args() 
    # Log.info("name arg -> %s", arg_inputs.Name)
    # cli_args
    # Log.info("name arg -> %s", cli_args().Name)
    # Log.info("Value arg -> %s", cli_args().Value)
    # tcgui_rules()

    if (cli_args().Name and cli_args().Value and cli_args().Delay):
        instanceScript = Iperf3toGoogleSheets(cli_args().Name,cli_args().Value, cli_args().Delay)
    # elif (cli_args().Delay):
    #     instanceScript = Iperf3toGoogleSheets(cli_args().Delay)

    else:
        instanceScript = Iperf3toGoogleSheets()

    # instanceScript = Iperf3toGoogleSheets()
    instanceScript.setup()
    instanceScript.tc_delay_command()
    # instanceScript.connected()
    # instanceScript.tc_delay_command(cli_args().Delay)
    instanceScript.data_manipulation_tcp()
    instanceScript.data_manipulation_udp()

