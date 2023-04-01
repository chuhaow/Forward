import numpy
import sys
import pandas as pd




def Forward(emissions, transition, dp):

    for c in range(1,dp.shape[1]):
        for r in range(1,dp.shape[0]):
            state = dp.index[r]
            alpha = dp.columns[c]
            eKey = (state, alpha)
            if( eKey in emissions and emissions[eKey] > 0):
                sum = 0
                for k in range(dp.shape[0]):
                    pastState = dp.index[k]
                    tKey = (pastState, state)
                    
                    if(tKey in transition and transition[tKey] > 0):
                        #print(dp.index.get_loc(pastState))
                        #print(dp.iloc[dp.index.get_loc(pastState)][c-1])
                        sum += dp.iloc[dp.index.get_loc(pastState)][c-1] * transition[tKey]
                        #print("Can transition from " + pastState + " From state " + state)

                dp.iloc[r][c] = sum * emissions[(state, alpha)]
            else:
                dp.iloc[r][c]  =0
                
            

            #dp.iloc[r][c] = r
    state = dp.index[dp.shape[0]-1]
    sum = 0
    for k in range(dp.shape[0]):
        pastState = dp.index[k]
        tKey = (pastState, state)
        
        if(tKey in transition and transition[tKey] > 0):
            #print(dp.index.get_loc(pastState))
            
            #print(dp.iloc[dp.index.get_loc(pastState)][c])
            sum += dp.iloc[dp.index.get_loc(pastState)][c] * transition[tKey]
            #print(c)
            #print("Can transition from " + pastState + " From state " + state)
    dp.iloc[dp.shape[0]-1][dp.shape[1]-1] = sum 
    print("Total Probability: " + str(dp.iloc[dp.shape[0]-1][dp.shape[1]-1]) )
    print("\n##### TABLE #####")
    print(dp)






def buildTable(states, output):

    states.insert(0,"B")
    states.append("E")
    dp = pd.DataFrame(columns=output, index=states)

    for i in range(1,dp.shape[0]):
        dp.iloc[i][0] = 0
    for i in range(1,dp.shape[1]):
        dp.iloc[0][i] = 0
    dp.iloc[0][0] = 1

    return dp




############
####MAIN####
############

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print("USAGE:  python  Forward.py  emissionsFile  transitionsFile output")
        sys.exit(0)

    emissionsFile = sys.argv[1]
    transitionsFile = sys.argv[2]
    output = sys.argv[3]
    pd.options.display.float_format = '{:.10e}'.format
    emissions = {}
    transition = {}
    states = []
    outputList = list(output)
    outputList.insert(0,"0")
    with open(emissionsFile, 'r') as e:
        alphabet = e.readline().strip().split('\t')
        for line in e:
            l = line.strip().split('\t')
            state = l[0]
            states.append(state)
            for i in range(1,len(l)):
                key = (state, alphabet[i-1])
                value = l[i]
                emissions[key] = float(value)
    
    #print(emissions)

    with open(transitionsFile,"r") as t:
        dest = t.readline().strip().split("\t")
        for line in t:
            l = line.strip().split('\t')
            source = l[0]
            for i in range(1,len(l)):
                key = (source, dest[i-1])
                value = l[i]
                transition[key] = float(value)
    
    #print(transition)

    dp = buildTable(states=states, output=outputList)
    Forward(emissions,transition,dp)

