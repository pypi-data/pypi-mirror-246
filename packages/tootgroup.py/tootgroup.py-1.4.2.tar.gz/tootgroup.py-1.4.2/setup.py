"""For building the Python package"""

import setuptools
import tootgroup_tools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tootgroup.py",
    version=tootgroup_tools.version.CURRENT,
    author="Andreas Schreiner",
    author_email="andreas.schreiner@sonnenmulde.at",
    description="Group account features on Mastodon, Pleroma and Friendica",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oe4dns/tootgroup.py",
    packages=setuptools.find_packages(),
    keywords="mastodon pleroma friendica toot group account fediverse",
    classifiers=[
        "Environment :: Console",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "Mastodon.py",
        "platformdirs",
    ],
    scripts=["tootgroup.py"],
)
