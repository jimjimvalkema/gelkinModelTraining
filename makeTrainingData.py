import json
import os 
import sys
import argparse

def makeCsv(inputFolder, label, maxAddrs=2000):
    csv = ""
    mountAddrs = 0
    for jsonFile in os.listdir(inputFolder):
        with open(inputFolder+"/"+jsonFile) as json_file:
            print("reading: {}".format(inputFolder+"/"+jsonFile))
            try:
                data = json.load(json_file)
            except:
                print("data bad :( : "+inputFolder+"/"+jsonFile)
                continue
                
        for addr in data:
            mountAddrs += 1
            toAddrsTxCount = {}
            amountsSend = []
            for tx in data[addr]:
                if tx['to_address'] in toAddrsTxCount:
                    toAddrsTxCount[tx['to_address']] += 1
                else:
                    toAddrsTxCount[tx['to_address']] = 1
                amountsSend.append(tx['value'])
            amountOfUniqueToAddrs = len(toAddrsTxCount) # TODO do address diversity
            modalTxAmount = getModal(amountsSend)

            #addressesList.append(amountOfUniqueToAddrs, modalTxAmount)
            csv += "{},{:f},{}\n".format(int(amountOfUniqueToAddrs), int(modalTxAmount), label)
            if mountAddrs > maxAddrs:
                return csv
    return csv
    
    
    
            

def getLargestKeyIntDict(intDict):
    if intDict==None:
        return 0
    largestKey=""
    for key in intDict:
        if largestKey == "" or intDict[largestKey] < intDict[key]:
            largestKey = key
    return largestKey

def getModal(intList):
    if intList == []:
        return 0
    else:
        intList.sort()
        return intList[int(len(intList)/2)]

# Try running with these args
#
# "Hello" 123 --enable
if __name__ == '__main__':
    
    if sys.version_info<(3,5,0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)
    csv = makeCsv("airdropfarmerstxhist","B",maxAddrs=2000)
    csv += makeCsv("airdropeligabletxhist","G",maxAddrs=2000)
    text_file = open("trainingData.csv", "w")
    n = text_file.write(csv)
    text_file.close()
