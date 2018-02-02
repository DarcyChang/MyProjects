"""
This module is used for detect which Cafe python package is missing and try to install it before
test execution if possible.
"""
__author__ = 'kelvin'
import sys, os
from getpass import getpass, getuser
import platform
plaf = platform.linux_distribution()

if plaf[0].upper() == "CENTOS":
    install_file = "init_centos_package.sh"
elif plaf[0].upper() == "UBUNTU":
    install_file = "init_ubuntu_package.sh"
else:
    install_file = None

def install_test():
    """
    To test if package in "packages list" are importable
    TODO: modify the package list into internal config file
    """
    packages = [
        'wget',
        'paramiko',
        'junit_xml',
        'pyshark',
        'dpath',
        'nose',
        'wget',
    ]
    for p in packages:
        try:
             __import__(p)
        except ImportError:
             #sys.stderr.writelines("python package '%s' not found" % p)
             raise ImportError("python package '%s' not found" % p)


def run_install_packages():
    """
    Current implementation install package thru setup/init_<os>_package.sh file
    """
    import inspect
    user = getuser()
    p = raw_input("To install missing packages,\nplease enter passwd for current user %s:" % user)
    path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

    install_script = os.path.join(path, "..", "..", "setup", install_file)
    ret = os.system("echo %s | sudo -S %s" % (p, install_script))
    if not ret == 0:
        sys.stderr.writelines("package installation script failed. exit")
        exit(-1)

def main():
    """
    Test if all packages are installed.

    If some of them are missing, run python package install shell script.

    Installation requires sudoer access.
    """
    try:
        install_test()
    except:
        if install_file:
            run_install_packages()
            install_test()
        else:
            raise RuntimeError("current OS is not supported")
            exit(-1)

if __name__ == "__main__":
    main()

