from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import os
import sys

class CustomInstall(install):
    def run(self):
        # Run the standard setuptools install process
        install.run(self)

        # Check if Node.js and npm are installed
        for command in ['node --version', 'npm --version']:
            try:
                subprocess.check_call(command, shell=True)
            except subprocess.CalledProcessError:
                print(f"Error: {command} failed. Node.js and npm must be installed.")
                sys.exit(1)

        # Define the directory where your Node.js code is located
        # The path is relative to the location of this setup.py file
        node_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'yol_app', 'trace_display')

        # Run `npm install` and `npm run build`
        for command in ['npm install', 'npm run build']:
            try:
                subprocess.check_call(command, shell=True, cwd=node_dir)
            except subprocess.CalledProcessError:
                print(f"Error: {command} failed.")
                sys.exit(1)

setup(
    cmdclass={
        'install': CustomInstall,
    },
    # The rest of the setup configuration will be read from setup.cfg
)