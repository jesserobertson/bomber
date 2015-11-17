import bomber
import unittest
import sys, os

class TestBomber(unittest.TestCase):

    """ Tests for Bomber imports
    """
    
    module = 'measurements'
    dset = None

    def setUp(self):
        self.mod = getattr(bomber, self.module)

    def test_datasets(self):
        self.assertIsNotNone(self.mod)
        self.assertIsNotNone(self.mod.DATASETS)
        self.assertIsNotNone(self.mod.URI)

    def test_get(self):
        get_method = getattr(self.mod, 'get_' + self.module)
        filename = get_method(self.dset)
        self.assertIsNotNone(filename)
        os.remove(filename)

# Dynamically generate test cases for each wavelet class
# We're going to iterate over all these wavelet classes and backends
# in a Cartesian manner, so that we test both the wavelet implementation
# and it's backend
modules = ('climate', 'measurements', 'classification')
for module in modules:
    for dset in getattr(bomber, module).DATASETS.keys():
        # Work out new name for test class from classes we're testing
        test_name = 'Test' + module.capitalize() + dset.capitalize()

        # Add new class to module
        sys.modules[__name__].__dict__[test_name] = type(
            test_name, (TestBomber,),
            dict(module=module, dset=dset))

# Clean up base class from module so it doesn't get picked up by the test
# suite loader
del sys.modules[__name__].__dict__['TestBomber']

if __name__ == '__main__':
    unittest.main(verbosity=2)