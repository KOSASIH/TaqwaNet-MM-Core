// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LendingContract {
    struct Loan {
        uint256 amount;
        uint256 interestRate; // in basis points (1/100th of a percent)
        uint256 duration; // in seconds
        address borrower;
        bool isActive;
    }

    mapping(address => uint256) public collateralBalances;
    mapping(address => Loan) public loans;

    event LoanRequested(address indexed borrower, uint256 amount, uint256 interestRate, uint256 duration);
    event LoanRepaid(address indexed borrower, uint256 amount);
    event CollateralDeposited(address indexed user, uint256 amount);
    event CollateralWithdrawn(address indexed user, uint256 amount);

    // Function to deposit collateral
    function depositCollateral() external payable {
        require(msg.value > 0, "Must deposit a positive amount");
        collateralBalances[msg.sender] += msg.value;
        emit CollateralDeposited(msg.sender, msg.value);
    }

    // Function to request a loan
    function requestLoan(uint256 amount, uint256 interestRate, uint256 duration) external {
        require(collateralBalances[msg.sender] > 0, "No collateral deposited");
        require(loans[msg.sender].isActive == false, "Existing loan must be repaid first");

        loans[msg.sender] = Loan({
            amount: amount,
            interestRate: interestRate,
            duration: duration,
            borrower: msg.sender,
            isActive: true
        });

        emit LoanRequested(msg.sender, amount, interestRate, duration);
    }

    // Function to repay a loan
    function repayLoan() external payable {
        Loan storage loan = loans[msg.sender];
        require(loan.isActive, "No active loan to repay");
        require(msg.value >= loan.amount + calculateInterest(loan.amount, loan.interestRate), "Insufficient repayment amount");

        // Mark loan as repaid
        loan.isActive = false;

        // Return collateral
        uint256 collateralAmount = collateralBalances[msg.sender];
        collateralBalances[msg.sender] = 0;
        payable(msg.sender).transfer(collateralAmount);

        emit LoanRepaid(msg.sender, loan.amount);
    }

    // Function to calculate interest
    function calculateInterest(uint256 amount, uint256 interestRate) public pure returns (uint256) {
        return (amount * interestRate) / 10000; // Convert basis points to percentage
    }

    // Function to withdraw collateral
    function withdrawCollateral(uint256 amount) external {
        require(collateralBalances[msg.sender] >= amount, "Insufficient collateral");
        require(loans[msg.sender].isActive == false, "Cannot withdraw collateral while loan is active");

        collateralBalances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);

        emit CollateralWithdrawn(msg.sender, amount);
    }

    // Function to check loan status
    function getLoanStatus() external view returns (Loan memory) {
        return loans[msg.sender];
    }
}
