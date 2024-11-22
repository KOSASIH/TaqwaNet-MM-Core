// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract InvestmentContract {
    struct Investment {
        address investor;
        uint256 amount;
        uint256 timestamp;
        bool withdrawn;
    }

    mapping(address => Investment[]) public investments;
    address public owner;

    event InvestmentMade(address indexed investor, uint256 amount, uint256 timestamp);
    event InvestmentWithdrawn(address indexed investor, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function invest() external payable {
        require(msg.value > 0, "Investment amount must be greater than zero");
        investments[msg.sender].push(Investment(msg.sender, msg.value, block.timestamp, false));
        emit InvestmentMade(msg.sender, msg.value, block.timestamp);
    }

    function withdraw(uint256 investmentIndex) external {
        Investment storage investment = investments[msg.sender][investmentIndex];
        require(!investment.withdrawn, "Investment already withdrawn");
        require(investment.amount > 0, "No investment found");

        investment.withdrawn = true;
        payable(msg.sender).transfer(investment.amount);
        emit InvestmentWithdrawn(msg.sender, investment.amount);
    }

    function getInvestments(address investor) external view returns (Investment[] memory) {
        return investments[investor];
    }
}
