#!/usr/bin/env python
import json
import sys
import os
import csv  # writing

'''
The class parses the log file collected over CAN bus
Example log file:
  Trying 172.20.10.3...
  Connected to 172.20.10.3.
  Escape character is '^]'.
  {"timestamp":139.330000,"bus":1,"id":"0x1a1","data":"0x00104000000000"}
  {"timestamp":139.355000,"bus":1,"id":"0x1a1","data":"0x00104000000000"}
  ...
@param <log_filename> it contains the data in above mentioned format
@param <column_format> it contains the desired column order
                       of the csv file
output file is stored in the local directory
'''


class CAN_Parser:

    def __init__(self, log_filename, column_format):
        # csv file
        self._csv_filename = None
        self._output_writer = None
        self._csv_handle = None
        self._csv_column_format = column_format
        # log file
        self._log_filename = log_filename
        try:
            self._log_reader = open(log_filename)
        except:  # cannot open the log file
            print 'Error opening the log file. Please check the file name'
            exit(1)

    '''
		This private function creates/overwrites a csv file
		naming convention -
		example: input file is abc.log or abc.txt
				output csv filename: abc.csv
	'''

    def _open_csv_file(self):
                # e.g. basename = abc.log
        _log_basename = os.path.basename(self._log_filename)
        # e.g. output file = abc.csv
        self._csv_filename = os.path.splitext(_log_basename)[0] + '.csv'
        # write in byte mode - required by python's csv library
        self._output_writer = open(self._csv_filename, "wb")
        self._csv_handle = csv.writer(self._output_writer)

    '''
		This public function parses the log file and outputs the data
		in the corresponding csv file
		output: <filename>.csv file in the local directory
	'''

    def parse_logfile(self):
        if self._csv_handle is None:
            self._open_csv_file()
        try:
            self._csv_handle.writerow(self._csv_column_format)  # insert title
            for _line in self._log_reader:
                # ---- read line in the log file
                # If the line doesn't start with '{' skip the line
                if "{" != _line[0]:
                    continue
                # ---- parse the log line
                data = json.loads(_line)
                # build a row based on the order of values in
                # _csv_column_format
                csv_row = []
                for val in self._csv_column_format:
                    # push the data if no key exists then push None
                    csv_row.append(data[val] if val in data else None)
                # ---- save it to the csv file
                self._csv_handle.writerow(csv_row)
        except:
            print "Error in parse_logfile function: Error writing logs"
        print "Success: parsed data is stored in", self._csv_filename
        self._log_reader.close()  # close the log file
        self._output_writer.close()  # close the csv file

if __name__ == "__main__":
    # define the desired column format for the csv output file
    output_column_format = ['timestamp', 'bus', 'id', 'data']

    args = sys.argv  # read the arguments
    if len(args) < 2:
        print 'usage: python CAN_Parser.py <filename>.log'
        exit(1)

    inp_log_file = args[1]  # e.g /home/test/test.log

    parser = CAN_Parser(args[1], output_column_format)
    parser.parse_logfile()
