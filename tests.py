import unittest
import modules.vk

class TestVK(unittest.TestCase):
    # проверка на валидность токена VK    
    def test_invalid_token(self):
        with self.assertRaises(KeyError): modules.vk.get_subs('rambler', '12345')


if __name__ == "__main__":
    unittest.main()