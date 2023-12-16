from distutils.core import setup

setup(
    name             = 'asciiTUI',
    version          = '1.2.2',
    author           = 'azzammuhyala',
    author_email     = 'azzammuhyala@gmail.com',
    description      = 'This is a library of tools for you to use with your needs for an attractive type of terminal (console) display.',
    url              = 'https://github.com/azzammuhyala/asciiTUI',
    keywords         = ['asciiTUI', 'ascii', 'tui', 'console', 'text-based', 'tools', 'attractive', 'terminal', 'basic-tools', 'text', 'art-ascii'],
    packages         = ['asciiTUI'],
    long_description = """This is a library of tools for you to use with your needs for an attractive type of terminal (console) display.
Type `print(dir(asciiTUI))` for further functions, then type `print(asciiTUI.<func>.__doc__)` for further document information of each function."""
)