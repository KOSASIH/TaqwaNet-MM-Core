# src/tests/test_blockchain.py

import pytest
from web3 import Web3
from solcx import compile_source

# Sample Solidity code for the lending contract
lending_contract_source = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LendingContract {
    struct Loan {
        uint256 amount;
        uint256 interestRate;
        uint256 duration;
        address borrower;
        bool isActive;
    }

    mapping(address => uint256) public collateralBalances;
    mapping(address => Loan) public loans;

    event LoanRequested(address indexed borrower, uint256 amount, uint256 interestRate, uint256 duration);
    event LoanRepaid(address indexed borrower, uint256 amount);
    event CollateralDeposited(address indexed user, uint256 amount);
    event CollateralWithdrawn(address indexed user, uint256 amount);

    function depositCollateral() external payable {
        require(msg.value > 0, "Must deposit a positive amount");
        collateralBalances[msg.sender] += msg.value;
        emit CollateralDeposited(msg.sender, msg.value);
    }

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

    function repayLoan() external payable {
        Loan storage loan = loans[msg.sender];
        require(loan.isActive, "No active loan to repay");
        require(msg.value >= loan.amount + calculateInterest(loan.amount, loan.interestRate), "Insufficient repayment amount");

        loan.isActive = false;

        uint256 collateralAmount = collateralBalances[msg.sender];
        collateralBalances[msg.sender] = 0;
        payable(msg.sender).transfer(collateralAmount);

        emit LoanRepaid(msg.sender, loan.amount);
    }

    function calculateInterest(uint256 amount, uint256 interestRate) public pure returns (uint256) {
        return (amount * interestRate) / 10000;
    }

    function withdrawCollateral(uint256 amount) external {
        require(collateralBalances[msg.sender] >= amount, "Insufficient collateral");
        require(loans[msg.sender].isActive == false, "Cannot withdraw collateral while loan is active");

        collateralBalances[msg.sender] -= amount;
        payable(msg.sender).transfer(amount);

        emit CollateralWithdrawn(msg.sender, amount);
    }

    function getLoanStatus() external view returns (Loan memory) {
        return loans[msg.sender];
    }
}
'''

@pytest.fixture
def lending_contract(w3, accounts):
    # Compile the contract
    compiled_sol = compile_source(lending_contract_source)
    contract_interface = compiled_sol['<stdin>:LendingContract']

    # Deploy the contract
    LendingContract = w3.eth.contract(
        abi=contract_interface['abi'],
        bytecode=contract_interface['bin']
    )
    tx_hash = LendingContract.constructor().transact({'from': accounts[0]})
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

    return w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=contract_interface['abi']
    )

def test_deposit_collateral(lending_contract, accounts):
    initial_balance = w3.eth.getBalance(accounts[0])
    deposit_amount = w3.toWei(1, 'ether')

    # Deposit collateral
    tx_hash = lending_contract.functions.depositCollateral().transact({
        'from': accounts[0],
        'value': deposit_amount
    })
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Check collateral balance
    assert lending_contract.functions.collateralBalances(accounts[0]).call() == deposit_amount

def test_request_loan(lending_contract, accounts):
    deposit_amount = w3.toWei(1, 'ether')

    # Deposit collateral
    lending_contract.functions.depositCollateral().transact({
        'from': accounts[0],
        'value': deposit_amount
    })
    
    # Request a loan
    loan_amount = w3.toWei(0.5, 'ether')
    interest_rate = 500  # 5%
    duration = 3600  # 1 hour

    tx_hash = lending_contract.functions.requestLoan(loan_amount, interest_rate, duration).transact({' from': accounts[0]})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Check loan status
    loan = lending_contract.functions.getLoanStatus().call()
    assert loan[0] == loan_amount
    assert loan[1] == interest_rate
    assert loan[2] == duration
    assert loan[3] == accounts[0]
    assert loan[4] is True  # Loan should be active

def test_repay_loan(lending_contract, accounts):
    deposit_amount = w3.toWei(1, 'ether')

    # Deposit collateral
    lending_contract.functions.depositCollateral().transact({
        'from': accounts[0],
        'value': deposit_amount
    })

    # Request a loan
    loan_amount = w3.toWei(0.5, 'ether')
    interest_rate = 500  # 5%
    duration = 3600  # 1 hour
    lending_contract.functions.requestLoan(loan_amount, interest_rate, duration).transact({'from': accounts[0]})

    # Repay the loan
    repayment_amount = loan_amount + lending_contract.functions.calculateInterest(loan_amount, interest_rate).call()
    tx_hash = lending_contract.functions.repayLoan().transact({
        'from': accounts[0],
        'value': repayment_amount
    })
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Check loan status
    loan = lending_contract.functions.getLoanStatus().call()
    assert loan[4] is False  # Loan should no longer be active

def test_withdraw_collateral(lending_contract, accounts):
    deposit_amount = w3.toWei(1, 'ether')

    # Deposit collateral
    lending_contract.functions.depositCollateral().transact({
        'from': accounts[0],
        'value': deposit_amount
    })

    # Request a loan
    loan_amount = w3.toWei(0.5, 'ether')
    interest_rate = 500  # 5%
    duration = 3600  # 1 hour
    lending_contract.functions.requestLoan(loan_amount, interest_rate, duration).transact({'from': accounts[0]})

    # Repay the loan
    repayment_amount = loan_amount + lending_contract.functions.calculateInterest(loan_amount, interest_rate).call()
    lending_contract.functions.repayLoan().transact({
        'from': accounts[0],
        'value': repayment_amount
    })

    # Withdraw collateral
    tx_hash = lending_contract.functions.withdrawCollateral(deposit_amount).transact({'from': accounts[0]})
    w3.eth.waitForTransactionReceipt(tx_hash)

    # Check collateral balance
    assert lending_contract.functions.collateralBalances(accounts[0]).call() == 0

def test_insufficient_collateral(lending_contract, accounts):
    # Attempt to request a loan without collateral
    with pytest.raises(Exception):
        lending_contract.functions.requestLoan(1000, 500, 3600).transact({'from': accounts[0]})

def test_withdraw_collateral_while_loan_active(lending_contract, accounts):
    deposit_amount = w3.toWei(1, 'ether')

    # Deposit collateral
    lending_contract.functions.depositCollateral().transact({
        'from': accounts[0],
        'value': deposit_amount
    })

    # Request a loan
    loan_amount = w3.toWei(0.5, 'ether')
    interest_rate = 500  # 5%
    duration = 3600  # 1 hour
    lending_contract.functions.requestLoan(loan_amount, interest_rate, duration).transact({'from': accounts[0]})

    # Attempt to withdraw collateral while loan is active
    with pytest.raises(Exception):
        lending_contract.functions.withdrawCollateral(deposit_amount).transact({'from': accounts[0]}) ```python
