import React from "react";

/**
 * Setting up a context that stores initialized contacts for interaction with react components.
 */
const ContractContex = React.createContext({
    safebayToken: null,
    safebayTokenSale: null,
    safebayTokenSaleAddress: null,
    kycContract: null,
    web3: null,
    accounts: null
}); 

export default ContractContex;