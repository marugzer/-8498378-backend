import unittest
from app import get_average_monthly_value_metrics_a
from process_json import process_json


class TestAPIA(unittest.TestCase):

    def test_get_average_monthly_value_metrics_a(self):

        result = get_average_monthly_value_metrics_a("col","2022-06-01","2023-07-01")        
        self.assertEqual(result, None)

    
