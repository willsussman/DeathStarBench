import matplotlib.pyplot as plt
import numpy as np

dir = '/home/ubuntu/DeathStarBench/socialNetwork/sweeps'

conns_step = 50
conns_min = 1
conns_max = 301 + conns_step


rate_step = 200
rate_min = 1
rate_max = 2001 + rate_step


def main():
    data = {}
    for conns in range(conns_min, conns_max, conns_step):
        data[conns] = {}
        for rate in range(rate_min, rate_max, rate_step):
            # print(f'Reading {dir}/conns={conns}/rate={rate}/wrk.txt...')
            # f = open(f'{dir}/conns={conns}/rate={rate}/wrk.txt', 'r')
            # duration = float(f.read().split(' requests in ')[1].split('s, ')[0])
            # f.close()
            # print(duration)

            print(f'Reading {dir}/conns={conns}/rate={rate}/0.txt...')
            f = open(f'{dir}/conns={conns}/rate={rate}/0.txt', 'r')
            latencies = [int(y) for y in f.read().split('\n')[:-1]]
            # print(latencies)
            f.close()

            data[conns][rate] = latencies

    for conns in range(conns_min, conns_max, conns_step):
        plt.figure()
        plt.xlabel('Time')
        plt.ylabel('Latency')
        plt.title(f'-c {conns}')
        for rate in range(rate_min, rate_max, rate_step):
            latencies = data[conns][rate]
            X = np.linspace(0.0, 30.0, len(latencies))
            plt.plot(X, latencies, label=f'-R {rate}')
        plt.legend()
        print(f'Saving /home/ubuntu/DeathStarBench/socialNetwork/plots/conns/c{conns}.pdf...')
        plt.savefig(f'/home/ubuntu/DeathStarBench/socialNetwork/plots/conns/c{conns}.pdf')
        plt.close()
    
    for rate in range(rate_min, rate_max, rate_step):
        plt.figure()
        plt.xlabel('Time')
        plt.ylabel('Latency')
        plt.title(f'-R {rate}')
        for conns in range(conns_min, conns_max, conns_step):
            latencies = data[conns][rate]
            X = np.linspace(0.0, 30.0, len(latencies))
            plt.plot(X, latencies, label=f'-c {conns}')
        plt.legend()
        print(f'Saving /home/ubuntu/DeathStarBench/socialNetwork/plots/rate/R{rate}.pdf...')
        plt.savefig(f'/home/ubuntu/DeathStarBench/socialNetwork/plots/rate/R{rate}.pdf')
        plt.close()

if __name__ == "__main__":
    main()