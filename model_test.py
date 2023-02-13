# -*- coding: utf-8 -*-

import unittest

from model import Task


class TaskModelTaskCases(unittest.TestCase):
    def test_task_assembler(self):
        prefix_ends_with_slash = Task(prefix='https://example.com/prefix/', key_name='aes_256.key', m3u8_filename='index_6m.m3u8', download_dir='/path/to/storage')
        prefix_ends_without_slash = Task(prefix='https://example.com/prefix', key_name='aes_256.key', m3u8_filename='index_6m.m3u8', download_dir='/path/to/storage')
        self.assertEqual(prefix_ends_with_slash.key_url(), prefix_ends_without_slash.key_url())
        self.assertEqual(prefix_ends_with_slash.m3u8_url(), prefix_ends_without_slash.m3u8_url())
        print(prefix_ends_with_slash.key_url())
        print(prefix_ends_with_slash.m3u8_url())
        print(prefix_ends_without_slash.key_url())
        print(prefix_ends_without_slash.m3u8_url())


if __name__ == '__main__':
    unittest.main()
