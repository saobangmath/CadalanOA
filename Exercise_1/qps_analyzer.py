from collections import defaultdict 
import subprocess, time, os  
import matplotlib.pyplot as plt 

def readFile(filename):
    file = open(filename, "r")
    lines = file.readlines()
    fromStartTimeToCounter = defaultdict(lambda: 0)
    for line in lines: 
        l = line.split(",")
        fromStartTimeToCounter[l[0]] += 1
    
    plt.ylabel("qps")
    plt.plot(fromStartTimeToCounter.values())
    plt.show() 
    os.remove(filename)
    

def run_client(seconds: int):
    client_process = subprocess.Popen("make start_client", shell=True)
    print("done run client")
    time.sleep(seconds)
    print(f'sleep {seconds}')
    client_process.terminate()
    print("terminated!")


if __name__ == "__main__":
    run_client(10)
    readFile("async-debug.log")
