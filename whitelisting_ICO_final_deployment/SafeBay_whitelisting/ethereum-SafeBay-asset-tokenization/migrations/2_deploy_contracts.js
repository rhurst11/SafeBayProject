// For loading initial supply amount from environment file 
// (via "dotenv" library)
require("dotenv").config({"path": "../.env"});

var SafeBayToken = artifacts.require("./SafeBayToken.sol");
var SafeBayTokenSale = artifacts.require("./SafeBayTokenSale.sol"); 
var KYC = artifacts.require("./KYCContract.sol");

module.exports = async function (deployer) {
    let tokenSupply = process.env.INITIAL_TOKEN_SUPPLY;
    let address = await web3.eth.getAccounts();

    // Creating/minting new ERC-20 token with given initial supply
    await deployer.deploy(SafeBayToken, tokenSupply);

    // Creating KYC contract
    await deployer.deploy(KYC);

    // Creating crowdsale contract
    await deployer.deploy(SafeBayTokenSale, 1, address[0], SafeBayToken.address, KYC.address);
    
    // Transfering the ownership of tokens to the crowdsale contract
    let instance = await SafeBayToken.deployed();
    await instance.transfer(SafeBayTokenSale.address, tokenSupply);
};
