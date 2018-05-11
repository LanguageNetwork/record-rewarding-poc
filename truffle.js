var HDWalletProvider = require("truffle-hdwallet-provider");

var ropsten_account = "0xa37288ca4E6562045b66fD9482C68a22F3caA6b3";
var ropsten_mnemonic = "ginger assist wine pistol horn glass pledge hip calm round gas flower";

module.exports = {
    networks: {
        geth: {
            host: "localhost",
            port: 8545,
            network_id: "15",
            from: "0xaafe76dd70838c75e0c9253de3ff17e4db4714cb",
            gas: 4692388,
            gasPrice: 100000 // Specified in Wei
        },
        dev: {
            host: "localhost",
            port: 8545,
            network_id: "15",
            gas: 4692388,
            gasPrice: 100000 // Specified in Wei
        },
        ropsten: {
            provider: function () {
                return new HDWalletProvider(ropsten_mnemonic, "https://ropsten.infura.io/", 0);
            },
            network_id: "3",
            gas: 4692388,
            gasPrice: 32000000000, // Specified in Wei
            from: ropsten_account
        }
    },
    rpc: {
        host: "localhost",
        gas: 4692388,
        port: 8545
    },
    solc: {
        optimizer: {
            enabled: true,
            runs: 200
        }
    }
};