import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any

class CrowdfundingProject:
    def __init__(self, title: str, description: str, target_amount: float, duration_days: int, owner: str):
        self.id: str = str(uuid.uuid4())
        self.title: str = title
        self.description: str = description
        self.target_amount: float = target_amount
        self.current_amount: float = 0.0
        self.owner: str = owner
        self.start_date: datetime = datetime.now()
        self.end_date: datetime = self.start_date + timedelta(days=duration_days)
        self.donors: List[Dict[str, Any]] = []

    def donate(self, amount: float, donor: str) -> float:
        """Process a donation to the project."""
        if datetime.now() > self.end_date:
            raise Exception("Project funding period has ended.")
        if amount <= 0:
            raise ValueError("Donation amount must be greater than zero.")
        
        self.current_amount += amount
        self.donors.append({"donor": donor, "amount": amount, "date": datetime.now()})
        return self.current_amount

    def is_funded(self) -> bool:
        """Check if the project has reached its funding goal."""
        return self.current_amount >= self.target_amount

    def get_status(self) -> str:
        """Get the current status of the project."""
        if self.is_funded():
            return "Funded"
        elif datetime.now() > self.end_date:
            return "Funding Period Ended"
        else:
            return "Ongoing"

class CrowdfundingService:
    def __init__(self):
        self.projects: Dict[str, CrowdfundingProject] = {}

    def create_project(self, title: str, description: str, target_amount: float, duration_days: int, owner: str) -> CrowdfundingProject:
        """Create a new crowdfunding project."""
        project = CrowdfundingProject(title, description, target_amount, duration_days, owner)
        self.projects[project.id] = project
        return project

    def get_project(self, project_id: str) -> CrowdfundingProject:
        """Retrieve a crowdfunding project by its ID."""
        return self.projects.get(project_id)

    def donate_to_project(self, project_id: str, amount: float, donor: str) -> float:
        """Donate to a specific crowdfunding project."""
        project = self.get_project(project_id)
        if project:
            return project.donate(amount, donor)
        raise Exception("Project not found.")

    def get_all_projects(self) -> List[CrowdfundingProject]:
        """Retrieve a list of all crowdfunding projects."""
        return list(self.projects.values())

    def get_project_status(self, project_id: str) -> str:
        """Get the status of a specific crowdfunding project."""
        project = self.get_project(project_id)
        if project:
            return project.get_status()
        raise Exception("Project not found.")

    def get_donors(self, project_id: str) -> List[Dict[str, Any]]:
        """Retrieve a list of donors for a specific project."""
        project = self.get_project(project_id)
        if project:
            return project.donors
        raise Exception("Project not found.")

# Example usage
if __name__ == "__main__":
    crowdfunding_service = CrowdfundingService()

    # Create a new project
    project = crowdfunding_service.create_project(
        title="Community Park Renovation",
        description="Renovating the local park to make it more accessible and enjoyable for everyone.",
        target_amount=5000.0,
        duration_days=30,
        owner="Alice"
    )

    print(f"Created project: {project.title} with ID: {project.id}")

    # Donate to the project
    crowdfunding_service.donate_to_project(project.id, 100.0, "Bob")
    crowdfunding_service.donate_to_project(project.id, 250.0, "Charlie")

    # Check project status
    status = crowdfunding_service.get_project_status(project.id)
    print(f"Project Status: {status}")

    # List all donors
    donors = crowdfunding_service.get_donors(project.id)
    print("Donors:")
    for donor in donors:
        print(f"Donor: {donor['donor']}, Amount: {donor['amount']}, Date: {donor['date']}")
