from collections import defaultdict 
import subprocess, time, os  
import matplotlib.pyplot as plt 

class Resp: 
    def __init__(self):
        self.total = 0
        self.success = 0
        self.error_429s = 0
        self.error_400s = 0 
        self.error_403s = 0 
        self.error_401s = 0 
    def __repr__(self) -> str:
        return f'total:{self.total}, 200:{self.success}, 429:{self.error_429s}, 400: {self.error_400s}, 401: {self.error_401s}, 403: {self.error_403s}'


def readFile(filename):
    file = open(filename, "r")
    lines = file.readlines()
    timeStamptToResp = defaultdict(lambda: Resp())
    for line in lines: 
        l = line.split(",")
        timeStamptToResp[l[0]].total += 1 
        if (l[1].find("status 200")) != -1: 
            timeStamptToResp[l[0]].success += 1
        elif (l[1].find("status 400")) != -1: 
            timeStamptToResp[l[0]].error_400s += 1
        elif (l[1].find("status 401")) != -1: 
            timeStamptToResp[l[0]].error_401s += 1
        elif (l[1].find("status 403")) != -1: 
            timeStamptToResp[l[0]].error_403s += 1    
        elif (l[1].find("status 429")) != -1: 
            timeStamptToResp[l[0]].error_429s += 1            
    
    x = [_ for _ in range(len(timeStamptToResp))]
    success_rate = [resp.success/resp.total for resp in timeStamptToResp.values()]
    err_400_rate = [resp.error_400s/resp.total for resp in timeStamptToResp.values()]
    err_401_rate = [resp.error_401s/resp.total for resp in timeStamptToResp.values()]
    err_403_rate = [resp.error_403s/resp.total for resp in timeStamptToResp.values()]
    err_429_rate = [resp.error_429s/resp.total for resp in timeStamptToResp.values()]

    print(success_rate)

    plt.plot(x, success_rate, label = "200")
    plt.plot(x, err_400_rate, label = "400")
    plt.plot(x, err_401_rate, label = "401")
    plt.plot(x, err_403_rate, label = "403")
    plt.plot(x, err_429_rate, label = "429")
    
    plt.ylabel("percentage")
    leg = plt.legend(loc='lower right')
    
    plt.show()    

def clean_up(filename): 
    os.remove(filename)
    

def run_client(seconds: int):
    client_process = subprocess.Popen("make start_client", shell=True)
    time.sleep(seconds)
    client_process.terminate()


if __name__ == "__main__":
    run_client(60)
    readFile("async-debug.log")
    clean_up("async-debug.log")
