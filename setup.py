import os

from setuptools import setup

from pushbullet import __version__, __project_name__, __project_link__

def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
	name = __project_name__,
	version = __version__,
	author = 'Myles Braithwaite',
	author_email = 'me@mylesbraithwaite.com',
	description = 'A Python Library and a simple command line app for Pushbullet.',
	license = 'BSD',
	keywords = 'pushbullet',
	url = __project_link__,
	packages = [ 'pushbullet' ],
	long_description = read('README'),
	classifiers = [
		"Development Status :: 3 - Alpha",
		"Topic :: Utilities",
		"License :: OSI Approved :: BSD License",
	],
	install_requires = [
		'requests',
		'python-magic',
	],
	extras_require = {
		'cli': [ 'clint' ]
	},
	entry_points = {
		'console_scripts': [
			'pushbullet = pushbullet.cli:main [cli]',
		]
	}
)
