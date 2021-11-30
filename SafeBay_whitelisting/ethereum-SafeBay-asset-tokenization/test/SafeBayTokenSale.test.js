/**
 * Testing of a smart contract using chai library.
 * In order to test it, start Ganache and update the truffle.config file to reglect the Ganache network parameters.
 * Command: "truffle test".
 */

// For loading initial supply amount from environment file
// (via "dotenv" library)
require("dotenv").config({"path": "../.env"});

// Setting up testing environment
const chai = require("./setupChai");
const BN = web3.utils.BN;
const expect = chai.expect;

// Contracts for testing
const SafeBayToken = artifacts.require("./SafeBayToken.sol");
const SafeBayTokenSale = artifacts.require("./SafeBayTokenSale.sol");
const KYCContract = artifacts.require("./KYCContract.sol");

contract("SafeBayToken: Initial supply test", async (accounts) => {
    /**
     * We will test the migration of two contracts and the transfer of tokens.
     * Deploying the contracts through migrations file.
     */
    const [ owner, recipient, anotherAccount ] = accounts;

    it("All tokens are transfered to the Crowdsale contract", async () => {
        let instance = await SafeBayToken.deployed();
        
        // Owner has transfered all the tokens
        expect(instance.balanceOf(owner)).to.eventually.be.a.bignumber.equal(new BN(0));
        
        // Tokens are now with the Crowdsale contract
        let balanceOfSafeBayTokenSale = await instance.balanceOf(SafeBayTokenSale.address);
        let totalSupply = await instance.totalSupply();
        return expect(balanceOfSafeBayTokenSale).to.be.a.bignumber.equal(totalSupply);
    });
    
    it("Should be possible to buy tokens", async () => {
        let instanceSafeBayToken = await SafeBayToken.deployed();
        let instanceKYC = await KYCContract.deployed(); 
        let instanceSafeBayTokenSale = await SafeBayTokenSale.deployed();

        // Approve address through KYC so the user could buy
        instanceKYC.approveAddress(anotherAccount);

        // Sent ether to SafeBayTokenSale smart contract and receive tokens in return
        balanceBefore = await instanceSafeBayToken.balanceOf(anotherAccount);
        expect(instanceSafeBayTokenSale.sendTransaction({from: anotherAccount, value: web3.utils.toWei("1", "wei")})).to.be.fulfilled;
        return expect(instanceSafeBayToken.balanceOf(anotherAccount)).to.eventually.be.a.bignumber.equal(balanceBefore.add(new BN(1)));
    });
});