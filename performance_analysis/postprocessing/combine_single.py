import fire
import pandas as pd 
import numpy as np

def get_df( f ):
    capture = False
    timestamps = []
    data = []
    while line := f.readline():
        if capture:
            line = line.split(",")
            timestamps.append(int(line[0]))
            data.append(float(line[1]))
        if line == "##########\n":
            capture = True
    p = pd.DataFrame([timestamps, data]).T
    return p

def mergedfs( a, b, nearest_sec=1 ):
    sw_est = pd.merge_asof( a,  \
      b,  \
      left_on='timestamp', \
      right_on='timestamp',  \
      direction='nearest',  \
      tolerance=nearest_sec )
    return sw_est

def main( wfile, *logs  ):
    
    dfs = []
    for log in logs:
        if log == "." or \
           log == "/":
            continue
        with open(log, 'r') as f:
            df = get_df(f)
            log = log.split("/")[-1]
            df = df.rename( columns={0: "timestamp", 1: f"{log}"} )
            df = df.set_index("timestamp")
            dfs.append(df)
    s = dfs[0]
    for i in range(1, len(dfs)):
        s = mergedfs( s, dfs[i] )
    s = s.set_index("timestamp")
    s.to_csv( wfile+".csv" )
    data = s.to_numpy().flatten()
    with open(wfile+"_tail.csv", "a") as f:
        f.write("{}\n".format(np.percentile(data, 98)))

if __name__ == "__main__":
    fire.Fire(main)

