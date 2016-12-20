import imp
import os
import sys

module_name = 'scanslib'
here_dir = os.path.dirname(os.path.abspath(__file__))
module_path = os.path.join(here_dir, '../../')
sys.path.append(module_path)
fp, pathname, description = imp.find_module(module_name)
scanslib = imp.load_module(module_name, fp, pathname, description)


class TestUnitUtility:
    def test_unit_utility_target_date_is_valid(self):
        assert scanslib.Utility.target_date_is_valid('2016-12-01')

    def test_unit_utility_target_date_is_valid_false(self):
        assert not scanslib.Utility.target_date_is_valid('2016-12-01-12:01')
