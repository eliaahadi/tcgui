# TCGUI

A lightweight Python-based Web-GUI for Linux traffic control (`tc`) to set, view and delete traffic shaping rules. The Web-GUI is intended for short-term isolated testbeds or classroom scenarios and does not contain any security mechanisms.

No further changes are planned right now, but pull requests are welcome.

## Requirements

- Ubuntu 16.04 LTS
- `sudo apt-get install iperf3`
- `sudo apt-get install gspread`

## Overview
The purpose of this program is to show traffic control (TC) data between different computers, ROSnodes, and configurations.

![tables](tc_tables.png)
- The image above shows overview information of connections from office_pc to xcy_mini_pc connected to same router.
- The table layout has rate as table headers, while first column is delay data from 0 to 1000ms with Transmission Control Protocol (TCP) data on left and User Datagram Protocol (UDP).
- For set data not in those columns/rows, custom rate and delay can be used.


## Usage
- The google spreadsheet can be accessed [here](https://docs.google.com/spreadsheets/d/1T6ayTn8KCTebblzwLHIkHSnBUha2vw7puMHLEvrwTLE/edit#gid=555898294).
- First, setup another computer with iperf and alter lines 52 and 74 with that computer's IP in gheet.py.
- Have two terminals running, one with the server side computer running TCGUI and the other running just this command:
```
$ iperf3 -s
```
- To populate the spreadsheet and do tests, run commands from command line where # is variable number in this format:
```
/tcgui $ python gsheet.py --Name Rate --Value #MB --Delay #ms 
```
- Some examples:
  - For testing one value in TCP and UDP with 1MB rate and 0ms delay. This will show up in corresponding cell in table.
```
/tcgui $ python gsheet.py --Name Rate --Value 1MB --Delay 0ms 
```
  - For testing a custom rate value in TCP and UDP with custom delay not in table already (15MB rate, 250ms delay). This will show up in H20 cell.
```
/tcgui $ python gsheet.py --Name Rate --Value 15MB --Delay 250ms 
```
  - For testing multiple rate values (for example, write NA) in TCP and UDP with 500ms delay. This will show up for that row with given delay. This also applies to custom delays.
```
/tcgui $ python gsheet.py --Name Rate --Value NA --Delay 500ms 
```


## Summary of test data
- From XCY Mini PC to Office Computer using same router, the graph shows with rate as x variable and bits per second (bps) as y variable in graph.