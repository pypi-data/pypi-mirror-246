from setuptools import find_packages, setup

setup(
    name='alarmraj',
    version='0.1.1',
    author='Aryan Raj',
    description='THE ALARM CLOCK!!',
    packages = find_packages(),
    install_requires = ["setuptools", "argparse"],
    entry_points = {
        "console_scripts":[
            "alarmraj=alarmraj.alarm:main",
        ],
    },
    package_data = {"alarmraj": ["*.mp3"]},
    include_package_data = True
)