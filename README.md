# record-rewarding-poc 
[![CircleCI](https://circleci.com/gh/LanguageNetwork/record-rewarding-poc/tree/master.svg?style=svg)](https://circleci.com/gh/LanguageNetwork/record-rewarding-poc)

POC for token reward of the voice recording 

## Install dependencies

For OS X, you can use `brew` as well
```bash
$ apt install nodejs // Recommand nodejs >= 8.x.x
$ npm install truffle ganache-cli -g
```

## Run private blockchain network
There are two alternatives for run the test network.

### Use ganache-cli
```bash
// Install ganache-cli if you don't have
$ ganache-cli
```

### Use geth
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
// Use ganache-cli if you want to test
$ truffle test --network dev
```

## Compile & Migrate
```bash
// Compile the contract
$ truffle compile

// Ensure that you ran a geth network with http://localhost:8545 and network id should be 15
// Migrate contract to geth network with password
$ ACCOUNT_PASSWORD=1234 truffle migrate --network geth

Using network 'geth'.

Running migration: 1_initial_migration.js
>> Unlocking account 0xaafe76dd70838c75e0c9253de3ff17e4db4714cb
>> Deploying migration
  Deploying Migrations...
  ... 0xa9afee38779ee2acfb11b4c0895524c8a2c7a8b2c022b9cf8b3543640bb1d851
  Migrations: 0x7cd3689d55763349f264a4ac2a51450a5d8e9a88
Saving successful migration to network...
  ... 0x17152794bea44451d627ff31ccd097bf0dee08e1e35b8c1e3d745576a160afa9
Saving artifacts...
Running migration: 2_contract_migration.js
Network: geth
Deployer: [object Object]
BasicToken: function TruffleContract() {
        this.constructor = temp;
        return Contract.apply(this, arguments);
      }
  Deploying BasicToken...
  ... 0x24fd97c2bc5bf602dd1bfd2f43660d10ab6a4dbae5e04a922f7674e7c2e5f1a5
  BasicToken: 0x1265872bd9b5aad6bafe6dd6d004ac92ea4c6cf8
Saving successful migration to network...
  ... 0xdda9af1863e744b94825d08ffaf476eb7bdae92d076c49c42d6874002070238a
Saving artifacts...
```

## Run web3py script
```bash
$ python poc_web3.py       
  
Contract: 0x52Cd5A43489326D1a93E86316472fe01CaDA1b85
Before give token
My Balance: 0
0x3a2d4a0b6CC472852f74C158D4F748cdFd505e68 Balance: 0
0xC805fB24113Ee23089eb55c26B143890eFB42f66 Balance: 0
After give token
My Balance: 0
0x3a2d4a0b6CC472852f74C158D4F748cdFd505e68 Balance: 0
0xC805fB24113Ee23089eb55c26B143890eFB42f66 Balance: 1000
Done
```

