pragma solidity ^0.5.0;

import "openzeppelin-solidity/contracts/token/ERC20/ERC20.sol";
import "openzeppelin-solidity/contracts/math/SafeMath.sol";
import "openzeppelin-solidity/contracts/ownership/Ownable.sol";

/*STAKING TOKEN*/
/**
* @title Staking Token (STK)
* @author Alberto Cuesta Canada
* @notice Implements a basic ERC20 staking token with incentive distribution.
*/
contract StakingToken is ERC20, Ownable {
   using SafeMath for uint256;

   /**
    * @notice The constructor for the Staking Token.
    * @param _owner The address to receive all tokens on construction.
    * @param _supply The amount of tokens to mint on construction.
    */
   constructor(address _owner, uint256 _supply)
       public
   {
       _mint(_owner, _supply);
   }

/*STAKE HOLDERS*/
    /**
     * @notice We usually require to know who are all the stakeholders.
     */
    address[] internal stakeholders;

       /**
    * @notice A method to check if an address is a stakeholder.
    * @param _address The address to verify.
    * @return bool, uint256 Whether the address is a stakeholder,
    * and if so its position in the stakeholders array.
    */
   function isStakeholder(address _address)
       public
       view
       returns(bool, uint256)
   {
       for (uint256 s = 0; s < stakeholders.length; s += 1){
           if (_address == stakeholders[s]) return (true, s);
       }
       return (false, 0);
   }

   /**
    * @notice A method to add a stakeholder.
    * @param _stakeholder The stakeholder to add.
    */
   function addStakeholder(address _stakeholder)
       public
   {
       (bool _isStakeholder, ) = isStakeholder(_stakeholder);
       if(!_isStakeholder) stakeholders.push(_stakeholder);
   }

   /**
    * @notice A method to remove a stakeholder.
    * @param _stakeholder The stakeholder to remove.
    */
   function removeStakeholder(address _stakeholder)
       public
   {
       (bool _isStakeholder, uint256 s) = isStakeholder(_stakeholder);
       if(_isStakeholder){
           stakeholders[s] = stakeholders[stakeholders.length - 1];
           stakeholders.pop();
       }
   }

/*STAKES*/
   /**
    * @notice The stakes for each stakeholder.
    */
   mapping(address => uint256) internal stakes;

      /**
    * @notice A method to retrieve the stake for a stakeholder.
    * @param _stakeholder The stakeholder to retrieve the stake for.
    * @return uint256 The amount of wei staked.
    */
   function stakeOf(address _stakeholder)
       public
       view
       returns(uint256)
   {
       return stakes[_stakeholder];
   }

   /**
    * @notice A method to the aggregated stakes from all stakeholders.
    * @return uint256 The aggregated stakes from all stakeholders.
    */
   function totalStakes()
       public
       view
       returns(uint256)
   {
       uint256 _totalStakes = 0;
       for (uint256 s = 0; s < stakeholders.length; s += 1){
           _totalStakes = _totalStakes.add(stakes[stakeholders[s]]);
       }
       return _totalStakes;
   }

      /**
    * @notice A method for a stakeholder to create a stake.
    * @param _stake The size of the stake to be created.
    */
   function createStake(uint256 _stake)
       public
   {
       _burn(msg.sender, _stake);
       if(stakes[msg.sender] == 0) addStakeholder(msg.sender);
       stakes[msg.sender] = stakes[msg.sender].add(_stake);
   }

   /**
    * @notice A method for a stakeholder to remove a stake.
    * @param _stake The size of the stake to be removed.
    */
   function removeStake(uint256 _stake)
       public
   {
       stakes[msg.sender] = stakes[msg.sender].sub(_stake);
       if(stakes[msg.sender] == 0) removeStakeholder(msg.sender);
       _mint(msg.sender, _stake);
   }

/*REWARDS*/
   /**
    * @notice The accumulated rewards for each stakeholder.
    */
   mapping(address => uint256) internal rewards;
  
   /**
    * @notice A method to allow a stakeholder to check his rewards.
    * @param _stakeholder The stakeholder to check rewards for.
    */
   function rewardOf(address _stakeholder)
       public
       view
       returns(uint256)
   {
       return rewards[_stakeholder];
   }

   /**
    * @notice A method to the aggregated rewards from all stakeholders.
    * @return uint256 The aggregated rewards from all stakeholders.
    */
   function totalRewards()
       public
       view
       returns(uint256)
   {
       uint256 _totalRewards = 0;
       for (uint256 s = 0; s < stakeholders.length; s += 1){
           _totalRewards = _totalRewards.add(rewards[stakeholders[s]]);
       }
       return _totalRewards;
   }

      /**
    * @notice A simple method that calculates the rewards for each stakeholder.
    * @param _stakeholder The stakeholder to calculate rewards for.
    */
   function calculateReward(address _stakeholder)
       public
       view
       returns(uint256)
   {
       return stakes[_stakeholder] / 100;
   }

   /**
    * @notice A method to distribute rewards to all stakeholders.
    */
   function distributeRewards()
       public
       onlyOwner
   {
       for (uint256 s = 0; s < stakeholders.length; s += 1){
           address stakeholder = stakeholders[s];
           uint256 reward = calculateReward(stakeholder);
           rewards[stakeholder] = rewards[stakeholder].add(reward);
       }
   }

   /**
    * @notice A method to allow a stakeholder to withdraw his rewards.
    */
   function withdrawReward()
       public
   {
       uint256 reward = rewards[msg.sender];
       rewards[msg.sender] = 0;
       _mint(msg.sender, reward);
   }
}
   /*TESTING*/
contract('StakingToken', (accounts) => {
   let stakingToken;
   const manyTokens = BigNumber(10).pow(18).multipliedBy(1000);
   const owner = accounts[0];
   const user = accounts[1];

   before(async () => {
       stakingToken = await StakingToken.deployed();
   });

   describe('Staking', () => {
       beforeEach(async () => {
           stakingToken = await StakingToken.new(
               owner,
               manyTokens.toString(10)
           );
       });
       
       it('createStake creates a stake.', async () => {
           await stakingToken.transfer(user, 3, { from: owner });
           await stakingToken.createStake(1, { from: user });

           assert.equal(await stakingToken.balanceOf(user), 2);
           assert.equal(await stakingToken.stakeOf(user), 1);
           assert.equal(
               await stakingToken.totalSupply(), 
               manyTokens.minus(1).toString(10),
           );
           assert.equal(await stakingToken.totalStakes(), 1);
       });
       
       it('rewards are distributed.', async () => {
           await stakingToken.transfer(user, 100, { from: owner });
           await stakingToken.createStake(100, { from: user });
           await stakingToken.distributeRewards({ from: owner });
          
           assert.equal(await stakingToken.rewardOf(user), 1);
           assert.equal(await stakingToken.totalRewards(), 1);
       });

       it('rewards can be withdrawn.', async () => {
           await stakingToken.transfer(user, 100, { from: owner });
           await stakingToken.createStake(100, { from: user });
           await stakingToken.distributeRewards({ from: owner });
           await stakingToken.withdrawReward({ from: user });
          
           const initialSupply = manyTokens;
           const existingStakes = 100;
           const mintedAndWithdrawn = 1;

           assert.equal(await stakingToken.balanceOf(user), 1);
           assert.equal(await stakingToken.stakeOf(user), 100);
           assert.equal(await stakingToken.rewardOf(user), 0);
           assert.equal(
               await stakingToken.totalSupply(),
               initialSupply
                   .minus(existingStakes)
                   .plus(mintedAndWithdrawn)
                   .toString(10)
               );
           assert.equal(await stakingToken.totalStakes(), 100);
           assert.equal(await stakingToken.totalRewards(), 0);
       });
   })
})
