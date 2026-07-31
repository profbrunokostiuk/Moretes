from enum import Enum

from src.ui.main_screen import MainScreen
from src.ui.recommendation_screen import RecommendationScreen
from src.ui.test_add_screen import TestAddScreen
from src.ui.bug_add_screen import BugAddScreen
from src.ui.update_data_screen import UpdateDataScreen
from src.ui.add_step_screen import AddStepScreen


class Screen(Enum):
    Main = MainScreen
    Recommendation = RecommendationScreen
    AddTest = TestAddScreen
    Update = UpdateDataScreen
    AddStep = AddStepScreen
    AddBug = BugAddScreen


if __name__ == "__main__":
    s = Screen
    print(s.Main)
