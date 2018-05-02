var BasicToken = artifacts.require("./BasicToken.sol");

module.exports = function(deployer, network) {
    console.log('Network: ' + network);
    console.log('Deployer: ' + deployer);
    console.log('BasicToken: ' + BasicToken);
    deployer.deploy(BasicToken);
};
