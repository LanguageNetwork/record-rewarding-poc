# redistribution_poc 
[![CircleCI](https://circleci.com/gh/LanguageNetwork/redistribution_poc/tree/master.svg?style=svg)](https://circleci.com/gh/LanguageNetwork/redistribution_poc/tree/master) 

POC code for token redistribution 

## Install dependencies

For OS X, you can use `brew` as well
```bash
$ apt install nodejs // Recommand nodejs >= 8.x.x
$ npm install truffle ganache-cli -g
```

## Run private blockchain network
### Run ganache-cli
```bash
// Install ganache-cli if you don't have
$ ganache-cli
```

### Run geth
```bash  
$ cd $PROJECT_PATH

// init the network with genesis block
$ geth init ./genesis.json --datadir geth_data

// Run geth 
$ geth --datadir ./geth_data --networkid 15 --rpc --rpcapi="db,eth,net,web3,personal,web3" --verbosity 3
```

And open another window, type the following command

```bash
$ cd $PROJECT_PATH

// attach to the network
$ geth attach --datadir ./geth_data

// Unlock the first account
> web3.personal.unlockAccount(web3.personal.listAccounts[0], "1234", 15000);

// Start mining
> miner.start()
```

## Run contract test
```bash
$ truffle test
```

