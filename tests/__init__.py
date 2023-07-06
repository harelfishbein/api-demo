from unittest import main, TestCase

if __name__ == '__main__':
    main()
    
class TestRootMethod(TestCase):
    def test_root(self):
        self.assertEqual('foo'.upper(), 'FOO')