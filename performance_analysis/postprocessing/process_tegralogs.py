
import fire
import pandas as pd 

def main( tlog ):
    
    powers = []
    cols = []
    with open(tlog, 'r') as f:
        while line := f.readline():
            line = line.split(" ")
            lfiltered = []
            i = 0
            while i < len(line):
                if "VDD" in line[i] or \
                   "VIN" in line[i]: 
                    lfiltered.append(line[i])
                    lfiltered.append(line[i+1])
                    i += 2
                else:
                    i += 1
            lf = []
            capture = False 
            if len( cols ) == 0:
                capture = True
            for i in range(0, len(lfiltered), 2):
                if capture:
                    cols.append(lfiltered[i])
                p = lfiltered[i+1] 
                p = p.split("/")[0]
                p = p[:-2]
                lf.append( float(p) )
            lf.append( sum(lf) )
            powers.append( lf )
        cols.append( 'total' )
        powers = pd.DataFrame(powers, columns=cols)
        powers.to_csv( tlog+".power.csv", index=False )

if __name__ == "__main__":
    fire.Fire(main)
