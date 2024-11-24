# src/controllers/governance_controller.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from src.models.asset_tokenization import Asset, Token, Ownership

class GovernanceProposal:
    def __init__(self, proposal_id, description, creator_id, end_time):
        self.proposal_id = proposal_id
        self.description = description
        self.creator_id = creator_id
        self.end_time = end_time
        self.votes_for = 0
        self.votes_against = 0
        self.voters = set()  # To track who has voted

    def vote(self, user_id, support):
        if user_id in self.voters:
            raise Exception("User  has already voted.")
        if datetime.now() > self.end_time:
            raise Exception("Voting period has ended.")

        self.voters.add(user_id)
        if support:
            self.votes_for += 1
        else:
            self.votes_against += 1

    def result(self):
        return self.votes_for > self.votes_against

class GovernanceController:
    def __init__(self, session: Session):
        self.session = session
        self.proposals = {}

    def create_proposal(self, description, creator_id, duration_days=7):
        proposal_id = len(self.proposals) + 1
        end_time = datetime.now() + timedelta(days=duration_days)
        proposal = GovernanceProposal(proposal_id, description, creator_id, end_time)
        self.proposals[proposal_id] = proposal
        return proposal_id

    def vote_on_proposal(self, proposal_id, user_id, support):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        
        proposal = self.proposals[proposal_id]
        proposal.vote(user_id, support)

    def get_proposal_result(self, proposal_id):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        
        proposal = self.proposals[proposal_id]
        if datetime.now() <= proposal.end_time:
            raise Exception("Voting is still ongoing.")
        
        return proposal.result()

    def execute_proposal(self, proposal_id):
        if proposal_id not in self.proposals:
            raise Exception("Proposal does not exist.")
        
        proposal = self.proposals[proposal_id]
        if datetime.now() <= proposal.end_time:
            raise Exception("Voting is still ongoing.")
        
        if proposal.result():
            # Execute the proposal (this could involve changing asset parameters, etc.)
            print(f"Proposal {proposal_id} passed: {proposal.description}")
        else:
            print(f"Proposal {proposal_id} failed: {proposal.description}")

if __name__ == "__main__":
    # Example usage
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # Database setup (replace with your database URL)
    engine = create_engine('sqlite:///assets.db')
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    governance_controller = GovernanceController(session)

    # Create a new proposal
    proposal_id = governance_controller.create_proposal("Increase asset supply", creator_id=1)
    print(f"Created proposal with ID: {proposal_id}")

    # Simulate voting
    governance_controller.vote_on_proposal(proposal_id, user_id=1, support=True)
    governance_controller.vote_on_proposal(proposal_id, user_id=2, support=False)

    # Get proposal result
    if datetime.now() > governance_controller.proposals[proposal_id].end_time:
        result = governance_controller.get_proposal_result(proposal_id)
        print(f"Proposal result: {'Passed' if result else 'Failed'}")
        governance_controller.execute_proposal(proposal_id)
