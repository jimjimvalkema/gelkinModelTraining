#!/usr/bin/env python3
from web3 import Web3
import requests
import json
import argparse
import sys

def cmdline_args():
        # Make parser object
    p = argparse.ArgumentParser(description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    p.add_argument("addressfile",
                   help="json from MEW with wallets addrs")
    # p.add_argument("required_int", type=int,
    #                help="req number")
    # p.add_argument("--on", action="store_true",
    #                help="include to enable")
    # p.add_argument("-v", "--verbosity", type=int, choices=[0,1,2], default=0,
    #                help="increase output verbosity (default: %(default)s)")
                   
    # group1 = p.add_mutually_exclusive_group(required=True)
    # group1.add_argument('--enable',action="store_true")
    # group1.add_argument('--disable',action="store_false")

    return(p.parse_args())

params = {
    'module': 'account',
    'action': 'txlist',
    'address': '0xc5102fE9359FD9a28f877a67E36B0F050d81a3CC',
    'startblock': '0',
    'endblock': '99999999',
    'page': '1',
    'offset': '10',
    'sort': 'asc',
    'apikey': 'TKXTZ6DTUZ19MV8VWX6IC5IMSSATUIY7M4',
}

def test():
    w3 = Web3(Web3.HTTPProvider('http://geth.dappnode:8545'))
    print(w3.isConnected())

    addresses = ["0x0E8703CEE6013390B4f66fcb998fE286D50cA7E0"]

    for i in range(16126990,16601609):
        txs = w3.eth.get_block(i, full_transactions=True)['transactions']
        for tx in txs:
            #print(tx)
            if tx['from'] in addresses:
                print("0x"+''.join(format(x, '02x') for x in  tx['hash']) )
        if ( i % 10) == 0:
            print(i)

def get_addresses_MEW_json(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)
    print("Type:", type(data))
    return [i["address"] for i in data]

def get_tx_hist(addresses):
    histories = {}
    for addr in addresses:
        print("doing: {}".format(addr))
        params['address'] = addr
        response = requests.get('https://api.etherscan.io/api', params=params)
        histories[addr] = response.json()
    return histories

def parse_to_csv(histories):
    #csv = "address,hash,to,value,functionName\n"
    csv = ""
    for addr in histories:
        for tx in histories[addr]['result']:
            line = "{},{},{},{},{}\n".format(addr,tx['hash'],tx['to'],tx['value'],tx['functionName'])
            csv+=line
    print(csv)
    return csv

def getWithCovalant(addr):
    url = "https://api.covalenthq.com/v1/eth-mainnet/address/{}/transactions_v3/".format(addr)
            
    headers = {
        "accept": "application/json",
    }
        
    response = requests.get(url, headers=headers,auth=('ckey_0723787af3c94ebaab5479b9b4e', ''))
    if response.text != None:
        return json.loads(response.text)["data"]['items']

def makeTxHistDict(addrList, outputfilename,lastAddr=""):
    txHistDict = {}
    amountFiles = 0
    foundLastAddr = False
    addrsDone = 0
    if lastAddr == "":
        foundLastAddr = True
        
    for addr in addrList:
        addr = addr.strip()
        if addr == lastAddr:
            foundLastAddr=True
        if foundLastAddr:
            txHistDict[addr] = getWithCovalant(addr)
            if not len(txHistDict) % 10:
                print("{}/{}".format(addrsDone+len(txHistDict), len(addrList)))
            if not len(txHistDict) % 100:
                amountFiles +=1
                print(addr)
                with open("{}-{}".format(amountFiles,outputfilename), "w") as outfile:
                    json.dump(txHistDict, outfile)
                addrsDone += len(txHistDict)
                txHistDict = {}
    return amountFiles




# Try running with these args
#
# "Hello" 123 --enable
if __name__ == '__main__':
    
    if sys.version_info<(3,5,0):
        sys.stderr.write("You need python 3.5 or later to run this script\n")
        sys.exit(1)
    
    args = cmdline_args()
    #addreses = get_addresses_MEW_json(args.addressfile)
    text_file = open(args.addressfile.split(".")[0] +"_txhistory.csv", "a")
    file1 = open(args.addressfile, 'r')
    Lines = file1.readlines()[1:]
    makeTxHistDict(Lines,args.addressfile.split(".")[0]+"txhist.json",lastAddr="")
    
    #foundLasAddr = True
    # for line in Lines:
    #     if line.strip() == "0x46b2b5e0011bc7698cd787bc7a1a907071ad979b":
    #         foundLasAddr=True
    #     if foundLasAddr:
    #         txhist = get_tx_hist([line.strip()])
    #         csv = parse_to_csv(txhist)
    #         if csv == None:
    #             continue
    #         print(csv)
    #         text_file.write(csv)
    # text_file.close