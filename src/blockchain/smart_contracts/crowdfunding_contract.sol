// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Crowdfunding {
    struct Project {
        address payable owner;
        string title;
        string description;
        uint256 goal;
        uint256 raisedAmount;
        uint256 deadline;
        bool isCompleted;
        uint256 milestoneCount;
        mapping(uint256 => Milestone) milestones;
        mapping(address => uint256) backers;
        bool isRefundable;
    }

    struct Milestone {
        string description;
        uint256 targetAmount;
        uint256 raisedAmount;
        bool isAchieved;
    }

    mapping(uint256 => Project) public projects;
    uint256 public projectCount;

    event ProjectCreated(uint256 projectId, address owner, string title, uint256 goal, uint256 deadline);
    event Funded(uint256 projectId, address backer, uint256 amount);
    event MilestoneAchieved(uint256 projectId, uint256 milestoneId);
    event ProjectCompleted(uint256 projectId);
    event RefundIssued(uint256 projectId, address backer, uint256 amount);

    modifier onlyOwner(uint256 projectId) {
        require(msg.sender == projects[projectId].owner, "Not the project owner");
        _;
    }

    modifier projectExists(uint256 projectId) {
        require(projectId < projectCount, "Project does not exist");
        _;
    }

    modifier notCompleted(uint256 projectId) {
        require(!projects[projectId].isCompleted, "Project is already completed");
        _;
    }

    function createProject(string memory title, string memory description, uint256 goal, uint256 duration) public {
        require(goal > 0, "Goal must be greater than 0");
        require(duration > 0, "Duration must be greater than 0");

        Project storage newProject = projects[projectCount++];
        newProject.owner = payable(msg.sender);
        newProject.title = title;
        newProject.description = description;
        newProject.goal = goal;
        newProject.deadline = block.timestamp + duration;
        newProject.isCompleted = false;
        newProject.isRefundable = true;

        emit ProjectCreated(projectCount - 1, msg.sender, title, goal, newProject.deadline);
    }

    function fundProject(uint256 projectId) public payable projectExists(projectId) notCompleted(projectId) {
        Project storage project = projects[projectId];
        require(block.timestamp < project.deadline, "Funding period has ended");
        require(msg.value > 0, "Must send ether to fund");

        project.raisedAmount += msg.value;
        project.backers[msg.sender] += msg.value;

        emit Funded(projectId, msg.sender, msg.value);
    }

    function createMilestone(uint256 projectId, string memory description, uint256 targetAmount) public onlyOwner(projectId) notCompleted(projectId) {
        require(targetAmount > 0, "Target amount must be greater than 0");

        Project storage project = projects[projectId];
        Milestone storage newMilestone = project.milestones[project.milestoneCount++];
        newMilestone.description = description;
        newMilestone.targetAmount = targetAmount;
        newMilestone.raisedAmount = 0;
        newMilestone.isAchieved = false;
    }

    function fundMilestone(uint256 projectId, uint256 milestoneId) public payable projectExists(projectId) notCompleted(projectId) {
        Project storage project = projects[projectId];
        Milestone storage milestone = project.milestones[milestoneId];

        require(msg.value > 0, "Must send ether to fund");
        require(milestoneId < project.milestoneCount, "Milestone does not exist");
        require(!milestone.isAchieved, "Milestone already achieved");

        milestone.raisedAmount += msg.value;
        project.raisedAmount += msg.value;

        if (milestone.raisedAmount >= milestone.targetAmount) {
            milestone.isAchieved = true;
            emit MilestoneAchieved(projectId, milestoneId);
        }

        emit Funded(projectId, msg.sender, msg.value);
    }

    function completeProject(uint256 projectId) public onlyOwner(projectId) notCompleted(projectId) {
        Project storage project = projects[projectId];
        require(block.timestamp >= project.deadline, "Funding period has not ended");
        require(project.raisedAmount >= project.goal, "Funding goal not met");

        project.isCompleted = true;
        project.isRefundable = false;

        emit ProjectCompleted(projectId);
    }

    function issueRefund(uint256 projectId) public projectExists(projectId) {
        Project storage project = projects[projectId];
        require(project.isRefundable, "Refunds are not available");
        require(block.timestamp >= project.deadline, "Funding period has not ended");
        require(project.raisedAmount < project.goal, "Funding goal met, no refunds");

        uint256 amount = project.backers[msg.sender];
        require(amount > 0, "No funds to refund");

        project.backers[msg.sender] = 0;
        project.raisedAmount -= amount;
        payable(msg.sender).transfer(amount);

        emit RefundIssued(projectId, msg.sender, amount);
    }

    function getProjectDetails(uint256 projectId) public view projectExists(projectId) returns (
        address owner,
        string memory title,
        string memory description,
        uint256 goal,
        uint256 raisedAmount,
        uint256 deadline,
        bool isCompleted,
        uint256 milestoneCount
    ) {
        Project storage project = projects[projectId];
        return (
            project.owner,
            project.title,
            project.description,
            project.goal,
            project.raisedAmount,
            project.deadline,
            project.isCompleted,
            project.milestoneCount
        );
    }

    function getMilestoneDetails(uint256 projectId, uint256 milestoneId) public view projectExists(projectId) returns (
        string memory description,
        uint256 targetAmount,
        uint256 raisedAmount,
        bool isAchieved
    ) {
        Project storage project = projects[projectId];
        require(milestoneId < project.milestoneCount, "Milestone does not exist");

        Milestone storage milestone = project.milestones[milestoneId];
        return (
            milestone.description,
            milestone.targetAmount,
            milestone.raisedAmount,
            milestone.isAchieved
        );
    }
}
