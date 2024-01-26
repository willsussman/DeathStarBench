#!/usr/bin/python3

# from urllib.request import urlopen
import json
from datetime import datetime
import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np

services = [
    'user_mongodb',
    'url_shorten_memcached',
    'user_timeline_mongodb',
    'media_mongodb',
    'post_storage_memcached',
    'home_timeline_redis',
    'user_memcached',
    'social_graph_mongodb',
    'social_graph_redis',
    'url_shorten_mongodb',
    'post_storage_mongodb',
    'user_timeline_redis',
    'media_memcached',
]

def main():

    f = open('timing.txt', 'r')
    contents = f.read().split('\n')
    f.close()
    # print(contents)
    start = datetime.strptime(contents[0].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()
    # start = pd.to_datetime(contents[0].split(']')[0], format='[%a %b %d %H:%M:%S %Z %Y')
    print(start)
    # print(start.timestamp())
    injection = datetime.strptime(contents[1].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()
    # injection = pd.to_datetime(contents[1].split(']')[0], format='[%a %b %d %H:%M:%S %Z %Y')
    print(injection)
    stop = datetime.strptime(contents[2].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()
    # stop = pd.to_datetime(contents[2].split(']')[0], format='[%a %b %d %H:%M:%S %Z %Y')
    print(stop)
    # exit(0)

    f = open('0.txt', 'r')
    contents = f.read().split('\n')
    f.close()
    latencies_Y = [int(y) for y in contents[:-1]]
    latencies_X = np.linspace(0, stop - start, len(latencies_Y))
    print(latencies_X)
    # plt.figure()
    # plt.plot(latencies_X, latencies_Y)
    # plt.savefig('debug.pdf')
    # plt.close()
    # print(latencies)
    # exit(0)

    bits = {}
    # min_timestamp = None
    # max_timestamp = None
    for service in services:
        bits[service] = {}
        print()
        print(service)
        # url = 'http://localhost:5000/query-file'
        # f = urlopen(url)
        f = open(f'webhook_data/{service}_webhook_data.txt', 'r')
        # contents = f.read().decode('utf-8')
        contents = f.read()
        f.close()
        # print(contents)

        entries = contents.split('\n')[:-1]
        # print(entries[-1])

        # bits = {}

        # min_timestamp = None
        # max_timestamp = None
        for entry in entries:
            # print()
            # print(entry)
            entry_obj = json.loads(entry)
            alerts = entry_obj['alerts']
            for alert in alerts:
                # status = alert['status']
                # print(status)
                # if status == 'resolved':
                #     print('TODO: resolved')
                #     continue
                labels = alert['labels']
                print(labels)
                alertname = labels['alertname'] # 'RedisReplicationDown'
                # job = labels['job'] # 'home-timeline-redis-exporter'
                # if job == 'post-storage-memcached-exporter':
                #     print(alert)
                #     print()
                startsAt = alert['startsAt'] # 2023-12-18T01:21:00.138Z
                timestamp = datetime.strptime(startsAt, "%Y-%m-%dT%H:%M:%S.%fZ").timestamp()
                # if min_timestamp == None or timestamp < min_timestamp:
                #     min_timestamp = timestamp
                # if max_timestamp == None or timestamp > max_timestamp:
                #     max_timestamp = timestamp
                # fingerprint = alert['fingerprint']

                if 'NOT' in alertname:
                    bit = 0
                    alertname = alertname.replace('NOT ', '')
                    # print(alertname)
                    # exit(0)
                else:
                    bit = 1

                # if job == 'home-timeline-redis-exporter':
                #     print(timestamp)
                # try:
                #     bits[job].append((timestamp, bit))
                # except KeyError:
                #     bits[job] = [(timestamp, bit)]
                
                # if job not in bits.keys():
                #     bits[job] = {}
                # if alertname not in bits[job].keys():
                #     bits[job][alertname] = []
                if alertname not in bits[service].keys():
                    bits[service][alertname] = []

                # if job == 'post-storage-memcached-exporter':
                #     print(f'appending to alertname={alertname}')
                # bits[job][alertname].append((timestamp, bit))
                bits[service][alertname].append((timestamp, bit))
    
    # bits2 = {}
    # for job in bits.keys():
    #     bits2[job] = combine(bits[job])
    # print(max_timestamp)
    # exit(0)
    for job in bits.keys():
        # plt.figure()
        fig, ax = plt.subplots()
        twinax = ax.twinx()
        ax.set_xlabel('Time')
        ax.set_ylabel('Bits')
        twinax.set_ylabel('Latency')
        # print(f'xlim={start - .05*(stop - start)},{stop + .05*(stop - start)}')
        # plt.xlim(start - .05*(stop - start), stop + .05*(stop - start))
        plt.xlim(- .05*(stop - start), stop-start + .05*(stop - start))
        # print(f'xlim={start},{stop}')
        # plt.xlim(min(latencies_X), max(latencies_X))
        ax.set_ylim(-.05, 1.05)
        twinax.plot(latencies_X, latencies_Y)
        ax.axvline(injection - start, linestyle='dashed', color='black')
        for alertname in bits[job]:
            print(alertname)
            X = [t-start for (t, _) in bits[job][alertname]]
            Y = [b for (_, b) in bits[job][alertname]]
            X, Y = zip(*sorted(zip(X, Y), key=lambda x: x[0]))
            # print(f'X={X}')

            X2 = [X[0]]
            Y2 = [Y[0]]
            for i in range(1, len(X)):
                if X[i] > X[i-1]:
                    X2.append(X[i])
                    Y2.append(Y[i])
            X = X2
            Y = Y2
            # print(f'X2={X2}')

            # X = X+[stop]
            # Y = Y+[Y[-1]]
            # print(f'final X={X}')
            # exit(0)

            for i in range(len(X)):
                print(f'({X[i]},{Y[i]})')
            # plt.scatter(X, Y, label=alertname)
            # plt.plot(X, Y, linestyle='-', marker='o', label=alertname)
            ax.step(X, Y, where='post', linestyle='-', marker='o', label=alertname)
            # plt.scatter()
            # step2(X, Y, label=alertname)
            # plt.step([min_timestamp]+list(X)+[max_timestamp], [Y[0]]+list(Y)+[Y[-1]], where='post', linestyle='-', marker='', label=alertname)
            # plt.step(X+[max_timestamp], Y+[Y[-1]], where='post', linestyle='-', marker='o', label=alertname)
        plt.title(f'{job}')
        ax.legend()
        print(f'Saving to bitplots/{job}.pdf...')
        plt.savefig(f'bitplots/{job}.pdf')
        plt.close()
        print()

    #starting time
    # start = pd.Timestamp(minimum)
    #Ending time
    # end = pd.Timestamp(maximum)
    #np.linspace() method with the interval of 10
    # t = np.linspace(start.value, stop.value, 25)
    # print("linspace format:\n",t)
    #Converting into datetime Index
    # t = pd.to_datetime(t)
    # print("DateTime Index:\n",t)
    #Converting input into array
    # print(np.asarray(t))

    # totals = []
    # for button in t:
    #     total = 0
    #     for key in bits.keys():
    #         total += interpolate(button, bits[key])
    #     totals.append(total)
    # plt.figure()
    # plt.xlabel('Time of Button Push')
    # plt.ylabel('Number of High Bits Returned')
    # plt.ylim([-.5, 0.5+len(bits.keys())])
    # plt.step(t, totals, where='post', linestyle='-', marker='o')
    # plt.title('totals')
    # plt.savefig('bitplots/totals.pdf')
    # plt.close()

# def combine(dict):
    # dict[alertname] = [(timestamp, bit)]


def interpolate(x, data):
    data_x, data_y = [t for (t, _) in data], [b for (_, b) in data]
    if x < min(data_x):
        return 0
    if x >= max(data_x):
        return data_y[-1]
    for i in range(len(data_x)-1):
        if x >= data_x[i] and x < data_x[i+1]:
            return data_y[i]

# def step2(X, Y, label):
#     for i in range(len(X)-1):
#         plt.plot([X[i], X[i+1]], [Y[i], Y[i]])
#         plt.plot([X[i+1], X[i+1]], [Y[i], Y[i+1]])
#         plt.scatter(X, Y)

if __name__ == "__main__":
    # print('Entered parse.py')
    main()