import os


class Turion:
    def __init__(self):
        self.api_key = os.getenv("TURION_API_KEY")
        self.project_id = os.getenv("TURION_PROJECT_ID")
