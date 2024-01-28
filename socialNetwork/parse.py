#!/usr/bin/python3

# from urllib.request import urlopen
import json
from datetime import datetime
import matplotlib.pyplot as plt
# import pandas as pd
import numpy as np
import statistics
import sys
import pandas as pd
import ruptures as rpt

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

    # 'social_graph_service',
    # 'compose_post_service',
    # 'post_storage_service',
    # 'user_timeline_service',
    # 'url_shorten_service',
    # 'user_service',
    # 'media_service',
    # 'text_service',
    # 'unique_id_service',
    # 'user_mention_service',
    # 'home_timeline_service',
    # 'nginx_thrift',
    # 'media_frontend',
]

def main(dir, candidate, mem):

    combo = f'{dir}/combos/{candidate}/{mem}'
    f = open(f'{combo}/timing.txt', 'r')
    lines = f.read().split('\n')
    f.close()

    start = datetime.strptime(lines[0].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()
    injection = datetime.strptime(lines[1].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()
    stop = datetime.strptime(lines[2].split(']')[0], '[%a %b %d %H:%M:%S %Z %Y').timestamp()

    # f = open('wrk.txt', 'r')
    # duration = float(f.read().split(' requests in ')[1].split('s, ')[0])
    # f.close()

    f = open(f'{combo}/0.txt', 'r')
    latencies_us = [int(y) for y in f.read().split('\n')[:-1]]
    latencies_ms = [y/1000 for y in latencies_us]
    f.close()
    latencies_X = np.linspace(0, stop - start, len(latencies_ms))

    plt.figure()
    plt.title(f'{candidate} {mem}')
    plt.xlabel('Time (s)')
    plt.ylabel('Latency (ms)')
    plt.axvline(injection - start, linestyle='dashed', color='black')

    # https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
    # Another strategy is to apply two moving averages to a chart:
    # one longer and one shorter. When the shorter-term MA crosses
    # above the longer-term MA, it's a buy signal, as it indicates
    # that the trend is shifting up. This is known as a golden
    # cross. Meanwhile, when the shorter-term MA crosses below the
    # longer-term MA, it's a sell signal, as it indicates that the
    # trend is shifting down. This is known as a dead/death cross.

    # window = 150
    # rolling = pd.Series(latencies_ms).rolling(window)
    # means = rolling.mean()
    # stdevs = rolling.std()
    # short = 0.25
    # long = 0.1
    # latencies_ewma_short = ewma(latencies_ms, short)
    # latencies_ewma_long = ewma(latencies_ms, long)

    # algo = rpt.Pelt(model="l2", min_size=28)
    # algo.fit(impressions)
    # result = algo.predict(pen=1)

    # data = pd.read_csv(os.path.join(path, 'impressions.csv'), parse_dates=['Date'], usecols=['Date', 'Impressions'])
    # data.set_index("Date", inplace=True)
    # data = data.sort_index()
    latencies_df = pd.DataFrame({
        'latencies_X': latencies_X,
        'latencies_ms': latencies_ms,
        }).set_index('latencies_X')
    # print(latencies_df)
    # exit(1)

    # impressions = data["Impressions"].values.reshape(-1, 1)


    # print('\nmodel=rbf', flush=True)
    # algo = rpt.Pelt(model="rbf").fit(latencies_df)
    # for pen in range(9):
    #     print(f'pen={pen}', flush=True)
    #     result = algo.predict(pen=pen)
    #     print(result, flush=True)
    # # print('\nmodel=l1', flush=True)
    # # algo = rpt.Pelt(model="l1").fit(latencies_df)
    # # for pen in range(15):
    # #     print(f'pen={pen}', flush=True)
    # #     result = algo.predict(pen=pen)
    # #     print(result, flush=True)
    # print('\nmodel=l2', flush=True)
    # algo = rpt.Pelt(model="l2").fit(latencies_df)
    # for pen in range(15):
    #     print(f'pen={pen}', flush=True)
    #     result = algo.predict(pen=pen)
    #     print(result, flush=True)

    buttons_X = []
    thresh = 350
    # for i in range(window-1, len(latencies_ms)):
    for i in range(len(latencies_ms)):
        # if latencies_ewma[i] > mean + 3*stdev:
        # if latencies_ewma[i] - latencies_ewma[i-1] > stdev:
        if latencies_ms[i] > thresh:
        # if latencies_ms[i] > means[i] + 2*stdevs[i]:
        # if latencies_ewma_short[i] > latencies_ewma_long[i]:
            plt.axvline(latencies_X[i], linestyle='solid', color='red')
            buttons_X.append(latencies_X[i])
    plt.plot([0, stop-start], [thresh, thresh], linestyle='dashed', color='red')
    plt.plot(latencies_X, latencies_ms, label='raw')
    # plt.plot(latencies_X, latencies_ewma_short, label=f'ewma({short})')
    # plt.plot(latencies_X, latencies_ewma_long, label=f'ewma({long})')
    # plt.plot(latencies_X, means, label=f'rolling({window}) mean')
    # plt.plot(latencies_X, means + 2*stdevs, label=f'rolling({window}) mean + 2sd')

    # plt.legend()
    print(f'Saving {combo}/latency.pdf...')
    plt.savefig(f'{combo}/latency.pdf')
    # exit(0)
    # latencies_X = np.linspace(0.0, duration, len(latencies_Y))
    # latencies_Y = [int(y) for y in contents[:-1]]
    # latencies_X = np.linspace(0, stop - start, len(latencies_Y))
    # print(latencies_X)
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
        f = open(f'{dir}/webhook_data/{service}_webhook_data.txt', 'r')
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
    button_elts = {}
    for job in bits.keys():
        # plt.figure()
        # fig, ax = plt.subplots()
        plt.figure()
        # twinax = ax.twinx()
        plt.xlabel('Time')
        plt.ylabel('Bits')
        # twinax.set_ylabel('Latency')
        # print(f'xlim={start - .05*(stop - start)},{stop + .05*(stop - start)}')
        # plt.xlim(start - .05*(stop - start), stop + .05*(stop - start))
        # plt.xlim(- .05*(stop - start), (stop - start) + .05*(stop - start))
        plt.xlim(0, stop - start)
        # print(f'xlim={start},{stop}')
        # plt.xlim(min(latencies_X), max(latencies_X))
        plt.ylim(-.05, 1.05)
        # twinax.plot(latencies_X, latencies_Y)
        plt.axvline(injection - start, linestyle='dashed', color='black')
        for x in buttons_X:
            plt.axvline(x, linestyle='solid', color='red')
        button_bits = []
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

            if len(buttons_X) > 0 and interpolate(X, Y, buttons_X[0]):
                button_bits.append(alertname)

            X = X+[stop-start]
            Y = Y+[Y[-1]]
            # print(f'final X={X}')
            # exit(0)

            # X = X+[32]
            # Y = Y+[Y[-1]]

            for i in range(len(X)):
                print(f'({X[i]},{Y[i]})')
            # plt.scatter(X, Y, label=alertname)
            # plt.plot(X, Y, linestyle='-', marker='o', label=alertname)
            plt.step(X, Y, where='post', linestyle='-', marker='', label=alertname)
            # plt.scatter()
            # step2(X, Y, label=alertname)
            # plt.step([min_timestamp]+list(X)+[max_timestamp], [Y[0]]+list(Y)+[Y[-1]], where='post', linestyle='-', marker='', label=alertname)
            # plt.step(X+[max_timestamp], Y+[Y[-1]], where='post', linestyle='-', marker='o', label=alertname)
        # print(f'button_bits={button_bits}')
        # if len(button_bits) > 0:
        button_elts[job] = button_bits
        plt.title(f'{job}')
        plt.legend()
        print(f'Saving {combo}/bitplots/{job}.pdf...')
        plt.savefig(f'{combo}/bitplots/{job}.pdf')
        plt.close()
        print()
    # print(f'len(buttons_X)={len(buttons_X)}')
    print(button_elts)

    output = {
        'button': (len(buttons_X) > 0),
        'elts': button_elts,
    }

    f = open(f'{combo}/button.json', 'w')
    json.dump(output, f)
    f.close()

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

def ewma(vec, alpha):
    out = [vec[0]]
    for i in range(1, len(vec)):
        out.append(alpha*vec[i] + (1-alpha)*out[i-1])
    return out

def interpolate(X, Y, x):
    # data_x, data_y = [t for (t, _) in data], [b for (_, b) in data]
    if x < X[0]:
        print('WARNING: button precedes first bit')
        return 0
    if x >= X[-1]:
        return Y[-1]
    for i in range(len(X)-1):
        if x >= X[i] and x < X[i+1]:
            return Y[i]

# def step2(X, Y, label):
#     for i in range(len(X)-1):
#         plt.plot([X[i], X[i+1]], [Y[i], Y[i]])
#         plt.plot([X[i+1], X[i+1]], [Y[i], Y[i+1]])
#         plt.scatter(X, Y)

if __name__ == "__main__":
    # print('Entered parse.py')
    if len(sys.argv) != 4:
        print('usage: parse.py DIRECTORY SERVICE MEMORY')
        exit(1)
    dir = sys.argv[1]
    candidate = sys.argv[2]
    mem = sys.argv[3]
    main(dir, candidate, mem)