import argparse

class Parse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="PPMJoyStick")
        self.parser.add_argument('--debug', action='store_true', help='Enable debug outputs')
        self.parser.add_argument('--raw', action='store_true', help='Show the raw values from radio.')
        self.args = self.parser.parse_args()
        self.debug = self.args.debug
        self.raw = self.args.raw
    
    def arguments(self):
        return self.args