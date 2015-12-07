import os
import sys
import subprocess

mydir = os.path.abspath(os.path.dirname(__file__))
example_dir = os.path.join(mydir, '..', 'example')

def test_example():
    subprocess.check_call([
        sys.executable,
        os.path.join(example_dir, 'build.py'),
        'build'
    ], cwd=example_dir)
