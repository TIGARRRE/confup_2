import unittest
import toml
from unittest.mock import patch
from collections import defaultdict
config = toml.load('config.toml')
from main import clean_version, get_dependencies, generate_png  # Ensure 'main' matches your filename

# Load the configuration file
config = toml.load('config.toml')

class TestFunctions(unittest.TestCase):

    def setUp(self):
        # Reset global variables before each test
        global all_dependencies, visited
        all_dependencies = defaultdict(set)
        visited = set()

    def test_clean_version(self):
        self.assertEqual(clean_version("1.2.3"), "1.2.3")
        self.assertEqual(clean_version("version 2.3.4"), "2.3.4")
        self.assertEqual(clean_version("no version here"), None)
        self.assertEqual(clean_version("3.0.1-alpha"), "3.0.1")

    @patch('main.requests.get')  # Имитация requests.get
    def test_get_dependencies(self, mock_get):
        if all_dependencies != 0:
            check = True

    @patch('main.subprocess.run')  # Mock subprocess.run
    def test_generate_png(self, mock_run):
        mock_run.return_value = None
        generate_png()
        mock_run.assert_called_once_with([config['graphviz_path'], '-Tpng', 'graph.dot', '-o', "base.png"], check=True)

if __name__ == '__main__':
    unittest.main()