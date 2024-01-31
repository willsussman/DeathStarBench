import sys
import os
import json
import pandas as pd

mems = ['512M', '256M', '128M', '64M', '32M', '16M', '8M'] # 'off'
cpus = ['1', '0.5', '0.25', '0.125', '0.0625', '0.03125', '0.015625']
# mems = ['512M', '256M'] # 'off'
# cpus = ['1', '0.5']
candidates = [
    'user-mongodb',
    'url-shorten-memcached',
    'user-timeline-mongodb',
    'media-mongodb',
    'post-storage-memcached',
    'home-timeline-redis',
    'user-memcached',
    'social-graph-mongodb',
    'social-graph-redis',
    'url-shorten-mongodb',
    'post-storage-mongodb',
    'user-timeline-redis',
    'media-memcached',

    'social-graph-service',
    'compose-post-service',
    'post-storage-service',
    'user-timeline-service',
    'url-shorten-service',
    'user-service',
    'media-service',
    'text-service',
    'unique-id-service',
    'user-mention-service',
    'home-timeline-service',
]

def main(dirname):
    # results = {}
    table = {}
    for candidate in candidates:
        # results[candidate] = {}
        table[candidate] = {}
        for mem in mems:
            f = open(f'{dirname}/combos/{candidate}/mem/{mem}/button.json', 'r')
            data = json.load(f)
            # print()
            # print(f'candidate={candidate}, mem={mem}, data={data}')
            f.close()

            if data['button']:
                table[candidate][f'mem={mem}'] = f'{sum([(len(value)>0) for value in data["elts"].values()])}, {sum([len(value) for value in data["elts"].values()])}, {len(data["elts"][candidate.replace("-","_")])>0}'
            else:
                table[candidate][f'mem={mem}'] = '-'
        for cpu in cpus:
            f = open(f'{dirname}/combos/{candidate}/cpu/{cpu}/button.json', 'r')
            data = json.load(f)
            # print()
            # print(f'candidate={candidate}, mem={mem}, data={data}')
            f.close()

            if data['button']:
                table[candidate][f'cpu={cpu}'] = f'{sum([(len(value)>0) for value in data["elts"].values()])}, {sum([len(value) for value in data["elts"].values()])}, {len(data["elts"][candidate.replace("-","_")])>0}'
            else:
                table[candidate][f'cpu={cpu}'] = '-'
    # print(results)
    df = pd.DataFrame(table).transpose()
    pd.set_option('display.max_rows', None)  # Replace None with a specific number if needed
    pd.set_option('display.max_columns', None)  # Replace None with a specific number if needed
    pd.set_option('display.width', 1000)  # Adjust the width to fit your screen
    # print(df, file=open('output.txt', 'a'))
    print(df)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('usage: summary.py DIRECTORY')
        exit(1)
    dirname = sys.argv[1]
    main(dirname)