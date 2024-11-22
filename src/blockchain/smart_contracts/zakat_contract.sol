// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ZakatContract {
    address public owner;
    uint256 public totalZakatCollected;

    event ZakatDonated(address indexed donor, uint256 amount);

    constructor() {
        owner = msg.sender;
    }

    function donateZakat() external payable {
        require(msg.value > 0, "Donation amount must be greater than zero");
        totalZakatCollected += msg.value;
        emit ZakatDonated(msg.sender, msg.value);
    }

    function withdrawZakat(address payable recipient) external {
        require(msg.sender == owner, "Only the owner can withdraw");
        recipient.transfer(address(this).balance);
    }

    function getTotalZakatCollected() external view returns (uint256) {
        return totalZakatCollected;
    }
}
