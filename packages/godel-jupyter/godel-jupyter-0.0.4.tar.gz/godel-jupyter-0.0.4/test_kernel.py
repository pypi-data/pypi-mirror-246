"""Example use of jupyter_kernel_test, with tests for IPython."""

import unittest
import jupyter_kernel_test as jkt


class BashKernelTests(jkt.KernelTests):
    kernel_name = "godel-jupyter"

    language_name = "rust"

    code_hello_world = 'predicate output(string hello) { hello = "hello, world" }'

    completion_samples = [
        {
            'text': 'fdis',
            'matches': {'fdisk'},
        },
    ]

    code_page_something = "ls?"

if __name__ == '__main__':
    unittest.main()