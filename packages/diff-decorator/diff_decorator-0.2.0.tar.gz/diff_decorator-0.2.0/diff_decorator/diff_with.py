import os
import functools
import unittest
import tempfile
import subprocess

# One could use vimdiff, meld, or even diff
def diff_with(test_func=None, tool=None):

    # Use DIFF_DECORATOR_TOOL env variable if set
    # otherwise default to diff
    default_tool = os.environ.get('DIFF_DECORATOR_TOOL', 'diff')
    tool = tool if tool is not None else default_tool

    # The decorator was used with parentheses
    # thus the test_func is not set, we need to call it ourself
    if test_func is None:
        return functools.partial(diff_with, tool=tool)

    def diff_to_files(diff_str):
        lines = diff_str.splitlines()

        expected_lines = []
        actual_lines = []

        for line in lines:
            if line.startswith('+ '):
                expected_lines.append(line[2:])
            elif line.startswith('- '):
                actual_lines.append(line[2:])
            elif line.startswith('  '):  # Two spaces for common lines
                expected_lines.append(line[2:])
                actual_lines.append(line[2:])

        return expected_lines, actual_lines

    @functools.wraps(test_func)
    def wrapper(test_case, *args, **kwargs):
        # Call the original test function
        try:
            result = test_func(test_case, *args, **kwargs)
        except AssertionError as e:
            expected_lines, actual_lines = diff_to_files(str(e))
            expected = '\n'.join(expected_lines)
            actual = '\n'.join(actual_lines)

            with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', prefix='expected_') as f1, \
                 tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.txt', prefix='actual_') as f2:

                f1.write(expected)
                f2.write(actual)
                f1.flush()
                f2.flush()

                # Call the tool to show differences
                subprocess.run([tool, f1.name, f2.name])

            raise  # re-raise the original exception

        return result

    return wrapper
