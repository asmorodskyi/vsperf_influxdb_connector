#!/usr/bin/python2

import argparse
import csv
import requests
import logging
import re
import os

def parse_csv(parsefile, os_version, os_build, vswitch_version, openqa_url):
    with open(parsefile, 'rb') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=',')
        for row in csvreader:
            request_string = 'throughput,testcase={0},traffic_type={1},' \
                .format(row['type'], row['traffic_type'])
            request_string += 'packetsize={0},vswitch={1},' \
                .format(row['packet_size'], row['vswitch'])
            request_string += 'os_version={0},os_build={1},vswitch_version={2},'.format(
                os_version, os_build, vswitch_version)
            request_string += 'openqa_url={0} value={1}'.format(
                openqa_url, row['throughput_rx_mbps'])
            logging.info('Posting data - {0}'.format(request_string))
            response = requests.post(url, data=request_string)
            logging.info('Response from DB: {0}'.format(response.content))


logging.basicConfig(filename='export.log', level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
parser = argparse.ArgumentParser()
parser.add_argument('--parsefile')
parser.add_argument('--parsefolder', default='/tmp')
parser.add_argument('--targeturl', default='http://fromm.arch.suse.de:8086')
parser.add_argument('--os_version')
parser.add_argument('--os_build')
parser.add_argument('--vswitch_version')
parser.add_argument('--openqa_url')
args = parser.parse_args()

url = args.targeturl + '/write?db=nfv_perf_data'

if args.parsefile:
    logging.info('Starting export. parserfile={0} targeturl={1}'
                 .format(args.parsefile, args.targeturl))
    parse_csv(args.parsefile, args.os_version, args.os_build,
              args.vswitch_version, args.openqa_url)
elif args.parsefolder:
    R = re.compile('results_.*')
    result_folders_list = [folder for folder in os.listdir(
        args.parsefolder) if R.match(folder)]
    for result_folder in result_folders_list:
        parsefile = '{0}/{1}/result_0_phy2phy_tput_p2p.csv'.format(
            args.parsefolder, result_folder)
        logging.info('Parsing file {0}'.format(parsefile))
        parse_csv(parsefile, args.os_version, args.os_build,
                  args.vswitch_version, args.openqa_url)
else:
    raise Exception('specify parsefolder or parsefile param')
