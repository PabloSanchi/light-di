from setuptools import find_packages, setup

setup(
	name="lightdi",
	version="0.1.0",
	description="A lightweight dependency injection module for Python.",
	long_description=open("README.md").read(),
	long_description_content_type="text/markdown",
	author="Pablo Sanchidrian",
	author_email="pablo.sanchi.herrera@gmail.com",
	url="https://github.com/PabloSanchi/light-di",
	packages=find_packages(),
	classifiers=[
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: Apache 2.0 License",
		"Operating System :: OS Independent",
	],
	python_requires=">=3.7",
	install_requires=[]
)
