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
            host:"localhost",
            port:8545,
            network_id: 3,
            from: "0x8F8d1bc97E8939e3932BfBeb923A1B2B972D5A9A",
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