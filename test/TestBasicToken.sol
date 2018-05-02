pragma solidity ^0.4.0;

// Test library
import "truffle/Assert.sol";
import "truffle/DeployedAddresses.sol";

// Our contract
import "../contracts/BasicToken.sol";


contract TestBasicToken {

    function testTruffleTest() public {
        uint expected = 1000;

        Assert.equal(1000, expected, "Comparing Integer");
    }

    function testDefaultTokenAmount() public {
        BasicToken node = new BasicToken();

        Assert.equal(node.myBalance(), 0, "The initial value for account should be 0");
    }

    function testGiveToken() public {
        BasicToken node = new BasicToken();

        // Give 100 tokens to owner of node
        node.giveToken(node.owner(), 100);

        Assert.equal(node.getBalance(node.owner()), 100, "Give token via giveToken()");
    }
}
