from setuptools import setup

setup(
        name = 'spotipy-tui',
        packages = ['spotipy_tui'],
        version = '1.0.5',
        include_package_data = True,
        description = 'Text-based UI to control Spotify client',
        author = 'Jonathan Chen',
        author_email = 'jonshepchen@gmail.com',
        license='MIT',
        entry_points={'console_scripts': ['spotipy-tui=spotipy_tui.app:run']},
        url = 'https://github.com/JonShepChen/SpotipyTUI',
        download_url = 'https://github.com/JonShepChen/SpotipyTUI/archive/v1.0.5.tar.gz',
        keywords = ['spotify', 'remote', 'audio', 'music', 'tui', 'curses'],
        install_requires=['requests'],
        classifiers = [
                'Intended Audience :: End Users/Desktop',
                'Environment :: Console :: Curses',
                'Operating System :: MacOS :: MacOS X',
                'Natural Language :: English',
                'Programming Language :: Python :: 3.1',
                'Programming Language :: Python :: 3.2',
                'Programming Language :: Python :: 3.3',
                'Programming Language :: Python :: 3.4',
                'Topic :: Terminals',
                'Topic :: Multimedia :: Sound/Audio :: Players',
              ],

        )
