pragma solidity ^0.5.0;

import "./SafeBayToken.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/Crowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/emission/AllowanceCrowdsale.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/crowdsale/validation/WhitelistCrowdsale.sol";

contract SafeBayAllowance is Crowdsale, AllowanceCrowdsale{
    constructor(
        uint rate, 
        address wallet,
        ERC20 token, 
        address tokenWallet,
    )
        Crowdsale(rate, wallet, token)
        AllowanceCrowdsale(tokenWallet)
        public
        {}
        
}