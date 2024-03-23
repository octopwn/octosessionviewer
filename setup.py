from setuptools import setup, find_packages
import re

VERSIONFILE="octosessionviewer/_version.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))


setup(
	# Application name:
	name="octosessionviewer",

	# Version number (initial):
	version=verstr,

	# Application author details:
	author="Tamas Jos",
	author_email="info@skelsecprojects.com",

	# Packages
	packages=find_packages(exclude=["tests*"]),

	# Include additional files into the package
	include_package_data=True,

	# Details
	url="https://github.com/octopwn/octosessionviewer",

	zip_safe = True,
	#
	# license="LICENSE.txt",
	description="",
	long_description="",

	python_requires='>=3.9',
	classifiers=(
		"Programming Language :: Python :: 3.6",
		"Operating System :: OS Independent",
	),
	install_requires=[
		'toml',
		'cryptography',
	],
	entry_points={
		'console_scripts': [
			'octopwn-session = octosessionviewer.__main__:main',
		],
	}
)
