#!/usr/bin/python2

import argparse
import csv
import requests

parser = argparse.ArgumentParser()
parser.add_argument('--parsefile', required=True)
parser.add_argument('--targeturl', default='http://fromm.arch.suse.de:8086')
args = parser.parse_args()

url = args.targeturl + '/write?db=data'
HW = 'aribeach-fromm'

with open(args.parsefile, 'rb') as csvfile:
    csvreader = csv.DictReader(csvfile, delimiter=',')
    for row in csvreader:
        request_string = 'throughput,testcase={0},traffic_type={1},packetsize={2},vswitch={3},hw={4} value={5}'.format(
            row['type'], row['traffic_type'], row['packet_size'], row['vswitch'], HW, row['throughput_rx_mbps'])
        print 'Will post {0} to {1} '.format(request_string, url)
        response = requests.post(url, data=request_string)
        print 'Response from DB: {0}'.format(response)
