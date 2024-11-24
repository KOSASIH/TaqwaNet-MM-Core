// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TaqwaNetCore is Ownable, ReentrancyGuard {
    struct Account {
        uint256 balance;
        bool isActive;
    }

    struct Investment {
        uint256 amount;
        uint256 startTime;
        uint256 maturityTime;
        bool isHalal;
    }

    mapping(address => Account) private accounts;
    mapping(address => Investment[]) private investments;

    event AccountCreated(address indexed user);
    event Deposit(address indexed user, uint256 amount);
    event Withdrawal(address indexed user, uint256 amount);
    event InvestmentMade(address indexed user, uint256 amount, bool isHalal);
    event ProfitDistributed(address indexed user, uint256 profit);

    IERC20 private stableToken;

    constructor(address _stableToken) {
        stableToken = IERC20(_stableToken);
    }

    modifier onlyActiveAccount() {
        require(accounts[msg.sender].isActive, "Account is not active");
        _;
    }

    // Create a new account
    function createAccount() external {
        require(!accounts[msg.sender].isActive, "Account already exists");
        accounts[msg.sender] = Account(0, true);
        emit AccountCreated(msg.sender);
    }

    // Deposit funds into the account
    function deposit(uint256 amount) external nonReentrant onlyActiveAccount {
        require(amount > 0, "Deposit amount must be greater than zero");
        stableToken.transferFrom(msg.sender, address(this), amount);
        accounts[msg.sender].balance += amount;
        emit Deposit(msg.sender, amount);
    }

    // Withdraw funds from the account
    function withdraw(uint256 amount) external nonReentrant onlyActiveAccount {
        require(amount > 0, "Withdrawal amount must be greater than zero");
        require(accounts[msg.sender].balance >= amount, "Insufficient balance");
        accounts[msg.sender].balance -= amount;
        stableToken.transfer(msg.sender, amount);
        emit Withdrawal(msg.sender, amount);
    }

    // Create a new investment
    function invest(uint256 amount, uint256 maturityTime, bool isHalal)
        external
        nonReentrant
        onlyActiveAccount
    {
        require(amount > 0, "Investment amount must be greater than zero");
        require(accounts[msg.sender].balance >= amount, "Insufficient balance");
        require(maturityTime > block.timestamp, "Invalid maturity time");

        accounts[msg.sender].balance -= amount;
        investments[msg.sender].push(
            Investment(amount, block.timestamp, maturityTime, isHalal)
        );
        emit InvestmentMade(msg.sender, amount, isHalal);
    }

    // Distribute profits based on Halal investments
    function distributeProfit(address user, uint256 profit) external onlyOwner {
        require(profit > 0, "Profit must be greater than zero");
        require(accounts[user].isActive, "Account is not active");

        accounts[user].balance += profit;
        emit ProfitDistributed(user, profit);
    }

    // Get account balance
    function getBalance() external view onlyActiveAccount returns (uint256) {
        return accounts[msg.sender].balance;
    }

    // Get investments for a user
    function getInvestments(address user)
        external
        view
        returns (Investment[] memory)
    {
        return investments[user];
    }

    // Check if account is active
    function isAccountActive(address user) external view returns (bool) {
        return accounts[user].isActive;
    }
}
