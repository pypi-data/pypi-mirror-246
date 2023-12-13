from setuptools import setup

setup(
    name='linktest',
    version='2.2.9',
    author='Wang Lin',
    author_email='think_wl@163.com',
    packages=['linktest'],
    install_requires=[
        "psutil",
        "requests",
        "pandas",
        "curlify",
        "selenium",
        "selenium-wire",
        "setuptools",
        "urllib3",
        "PyMySQL",
        "jsoncomparison",
        "chromedriver_autoinstaller"
    ],
)
