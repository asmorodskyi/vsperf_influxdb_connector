#!/usr/bin/python2

import argparse
import csv
import requests
import logging

logging.basicConfig(filename='export.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
parser = argparse.ArgumentParser()
parser.add_argument('--parsefile', required=True)
parser.add_argument('--targeturl', default='http://fromm.arch.suse.de:8086')
args = parser.parse_args()

url = args.targeturl + '/write?db=data'
HW = 'aribeach-fromm'

logging.info('Starting export. parserfile={0} targeturl={1} HW={2}'
             .format(args.parsefile, args.targeturl, HW))

with open(args.parsefile, 'rb') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    for row in csvreader:
        request_string = 'throughput,testcase={0},traffic_type={1},' \
            .format(row['type'], row['traffic_type'])
        request_string += 'packetsize={0},vswitch={1},hw={2} value={3}' \
            .format(row['packet_size'], row['vswitch'], HW,
                    row['throughput_rx_mbps'])
        logging.info('Posting data - {0}'.format(request_string))
        response = requests.post(url, data=request_string)
        logging.info('Response from DB: {0}'.format(response))
