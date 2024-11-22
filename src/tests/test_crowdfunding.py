import unittest
from src.services.crowdfunding_service import CrowdfundingService
from src.models.crowdfunding import CrowdfundingProject

class TestCrowdfundingService(unittest.TestCase):

    def setUp(self):
        self.crowdfunding_service = CrowdfundingService()

    def test_create_crowdfunding_project(self):
        project = CrowdfundingProject(title="New Project", goal_amount=10000, current_amount=0)
        result = self.crowdfunding_service.create_project(project)
        self.assertTrue(result, "The project should be created successfully.")

    def test_fund_crowdfunding_project(self):
        project = CrowdfundingProject(title="New Project", goal_amount=10000, current_amount=0)
        self.crowdfunding_service.create_project(project)
        result = self.crowdfunding_service.fund_project(project.id, 5000)
        self.assertEqual(project.current_amount, 5000, "The project should have 5000 as the current amount.")

    def test_project_goal_reached(self):
        project = CrowdfundingProject(title="New Project", goal_amount=10000, current_amount=9000)
        self.crowdfunding_service.create_project(project)
        self.crowdfunding_service.fund_project(project.id, 2000)
        self.assertTrue(project.is_goal_reached(), "The project goal should be reached.")

if __name__ == '__main__':
    unittest.main()
