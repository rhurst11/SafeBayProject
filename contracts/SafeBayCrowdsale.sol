pragma solidity ^0.5.0;

import "./SafeBayToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/MintedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/CappedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/TimedCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/RefundablePostDeliveryCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/distribution/PostDeliveryCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/PausableCrowdsale.sol";

// Have the KaseiCoinCrowdsale contract inherit the following OpenZeppelin:
// * Crowdsale
// * MintedCrowdsale
contract SafeBayCrowdsale is Crowdsale, MintedCrowdsale, CappedCrowdsale, PostDeliveryCrowdsale, TimedCrowdsale, RefundablePostDeliveryCrowdsale, PausableCrowdsale { 
    
    // Provide parameters for all of the features of your crowdsale, such as the `rate`, `wallet` for fundraising, and `token`.
    constructor(
        uint rate, //rate, in TKNbits
        address payable wallet, // wallet that raises the ether
        SafeBayToken token,  // the token
        uint goal, // amount of Ether the Crowsale is aiming to raise
        uint open, // opening time for Crowdsale
        uint close // closing time for Crowdsale 
    ) public 
        
        Crowdsale(rate, wallet, token)
        CappedCrowdsale(goal)
        TimedCrowdsale(open, close)
        RefundableCrowdsale(goal)
        PostDeliveryCrowdsale()
        PausableCrowdsale()
    {
        // constructor body can stay empty
    }
}


contract SafeBayCrowdsaleDeployer {
    // Create an `address public` variable called `kasei_token_address`.
    address public safebay_token_address;
    // Create an `address public` variable called `kasei_crowdsale_address`.
    address public safebay_crowdsale_address;

    // Add the constructor.
    constructor(
       string memory name,
       string memory symbol,
       address payable wallet, // this is the beneficiary address
       uint goal //set the crowdsale goal
    ) public {
        // Create a new instance of the KaseiCoin contract.
        SafeBayToken token = new SafeBayToken(name, symbol, 0);
        
        // Assign the token contract’s address to the `kasei_token_address` variable.
        safebay_token_address = address(token);

        // Create a new instance of the `KaseiCoinCrowdsale` contract
        SafeBayCrowdsale safebay_crowdsale = new SafeBayCrowdsale (1, wallet, token, goal, now, now + 14 weeks);
        
            
        // Aassign the `KaseiCoinCrowdsale` contract’s address to the `kasei_crowdsale_address` variable.
        safebay_crowdsale_address = address(safebay_crowdsale);

        // Set the `KaseiCoinCrowdsale` contract as a minter
        token.addMinter(safebay_crowdsale_address);
        
        // Have the `KaseiCoinCrowdsaleDeployer` renounce its minter role.
        token.renounceMinter();
    }
    
    
}