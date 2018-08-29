from setuptools import setup
import subprocess

def get_git_tag():
    try:
        rev = subprocess.check_output(['git', 'describe', '--tags', '--dirty']).decode('latin1').strip()
        rev = rev.split('-')
        if len(rev) == 1:
            return rev[0]
        if len(rev) == 2:
            if rev[1] == 'dirty':
                return f"{rev[0]}+{rev[1]}"
            else:
                return f"{rev[0]}.{rev[1]}"
        return f"{rev[0]}.{rev[1]}+{'.'.join(rev[2:])}"
    except subprocess.CalledProcessError:
        return None

def get_git_hash():
    try:
        rev = subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD']).decode('latin1').strip()
        return "0.0.0+" + rev
    except subprocess.CalledProcessError:
        return None

def get_version():
    fns = [
        get_git_tag,
        get_git_hash,
        lambda: "0.0.0"]

    version = None
    for i_fn in fns:
        version = i_fn()
        if version:
            break

    print(version)
    return version

setup(
    name='SVGExtractPoints',
    version=get_version(),
    author='Sven Peter',
    author_email='mail@svenpeter.me',
    url='https://github.com/svenpeter42/SVGExtractPoints',
    packages=['SVGExtractPoints'],
    include_package_data=True,
    entry_points={
        'console_scripts': ['SVGExtractPoints=SVGExtractPoints:main'],
    },
    install_requires= [
        'matplotlib',
    ],
)
