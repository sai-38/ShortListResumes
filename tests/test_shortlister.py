import unittest
from src.agents.shortlister_agent import ShortlisterAgent

class TestShortlisterAgent(unittest.TestCase):

    def setUp(self):
        self.agent = ShortlisterAgent()

    def test_shortlist(self):
        resumes = ["resume1.pdf", "resume2.pdf"]
        shortlisted = self.agent.shortlist(resumes)
        self.assertIsInstance(shortlisted, list)

    def test_get_shortlisted_candidates(self):
        self.agent.shortlist(["resume1.pdf", "resume2.pdf"])
        candidates = self.agent.get_shortlisted_candidates()
        self.assertGreater(len(candidates), 0)

if __name__ == '__main__':
    unittest.main()