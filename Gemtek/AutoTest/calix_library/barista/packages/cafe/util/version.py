import os
import sys
import re
import logging

import pip
# import pypm

from StringIO import StringIO
from contextlib import contextmanager
from ConfigParser import ConfigParser, NoOptionError, NoSectionError
from subprocess import check_output, CalledProcessError
from barista.client.management import Management


def __stdout_to_str(func, *args, **kwargs):
    """Call a Python method, intercept all writes to stdout, and return them as a string
    """
    io = StringIO()
    sys.stdout = io

    func(*args, **kwargs)

    sys.stdout = sys.__stdout__
    val = io.getvalue()

    return val


def __load_packageinfo(packageinfo_name="packageinfo"):
    """Read a Barista-format packageinfo file and return a ConfigParser object
    """
    packageinfo_path = Management.get_repo('cafe').strip() + os.path.sep + packageinfo_name
    c = ConfigParser()
    c.read(packageinfo_path)

    return c, packageinfo_path

def __extract(match_obj, group=1):
    """Extract the specified group from the match object and return it as string. If it cannot be retrieved
    (match_obj is None, or group does not exist), "UNKNOWN" returned.
    """
    if match_obj is None:
        ret = "UNKNOWN"
    else:
        try:
            ret = match_obj.group(group)
        except IndexError:
            ret = "UNKNOWN"

    return ret


def __get_cafe_version(conf):
    """Return the string representation of the current version of Cafe
    """
    try:
        version = conf.get('general', 'version')
    except (NoSectionError, NoOptionError):
        version = "UNKNOWN"

    return version

def __git_command(repo_path, *args):
    """Changes current directory to the Cafe git repo, executes the specified shell command (in subprocess,
    i.e. list format), and returns the output as a string
    """
    try:
        curdir = os.getcwd()
        file_path = repo_path
        os.chdir(file_path)

        s = check_output(args)
    finally:
        os.chdir(curdir)
    
    return s

def __get_git_refs(repo_path):
    """Get refs (branches, tags, etc.)  that are pointing to the current commit (HEAD)
    """
    ret = {}

    try:
        s = __git_command(repo_path, 'git', 'show-ref', 'HEAD').strip().split('\n')
    except CalledProcessError as e:
        s = ["UNKNOWN UNKNOWN"]

    for l in s:
        commit, ref = tuple(l.split())

        try:
            ret[commit]
        except KeyError:
            ret[commit] = [ref]
        else:
            ret[commit].append(ref)

    return ret

def __get_git_branch(repo_path):
    """Gets the currently active git branch
    """
    try:
        s = __git_command(repo_path, 'git', 'branch')
    except CalledProcessError:
        s = ""

    g = re.search("\*\s+(.+)", s)

    return __extract(g)


def __get_cafe_release_date(conf):
    """Reads the release date from packageinfo and returns it
    """
    try:
        rd = conf.get('general', 'release_date')
    except (NoSectionError, NoOptionError):
        rd = "UNKNOWN"

    return rd


def __get_lib_list(conf, pm):
    """Gets a list of libraries for the specified package manager (pip or pypm) and returns it
    """
    try:
        libs = conf.get('dependencies', pm).split()
    except (NoSectionError, NoOptionError):
        libs = []

    return libs


def __get_pip_lib_version(libname):
    """Retrieves the version of the specified library installed using pip
    """
    output = __stdout_to_str(pip.main, ['show', libname])
    g = re.search("Version:\s+(.+)", output)

    return __extract(g)


def __get_pypm_lib_version(libname):
    """Retrieves the version of the specified library installed using pypm
    """
    # output = __stdout_to_str(pypm.cmd, ['-g', 'show', libname])
    pypm_path = os.path.dirname(sys.executable) + os.path.sep + 'pypm'

    try:
        output = check_output([pypm_path, '-g', 'show', libname])
        g = re.search("Status:\s+Already\s+installed\s+\((.+?)\)", output)
        ret = __extract(g)
    except CalledProcessError:
        ret = "UNKNOWN"

    return ret


def get_version_info(cafe_version=True, lib_versions=True, git_info=True):
    """Returns a formatted string containing the current version of Cafe, versions of python libraries
    that Cafe depends on, as well as Cafe Git Repo information

    Args:
        cafe_version (bool): If True, "Cafe Version" section will be shown, otherwise not
        lib_versions (bool): If True, "PIP Library Versions" and "PyPM Library Versions" sections will
            be shown, otherwise not
        git_info (bool): If True, "Git Repository Information" section will be shown, otherwise not

    Returns:
        str: a formatted string containing version information

    """
    # logging.getLogger("pypm").setLevel(logging.ERROR)

    c, pkginfo_path = __load_packageinfo()

    pkginfo_path = os.path.dirname(pkginfo_path)

    ret = ""

    if cafe_version:
        ret += "\nCafe Version:\n"
        ret += "\n\tRelease Version - %s\n" % __get_cafe_version(c)
        ret += "\tRelease Date - %s\n" % __get_cafe_release_date(c)

    if lib_versions:
        piplibs = __get_lib_list(c, 'pip')
        pypmlibs = __get_lib_list(c, 'pypm')

        ret += "\nPIP Library Versions:\n\n"

        for i in piplibs:
            ret += "\t%s - %s\n" % (i, __get_pip_lib_version(i))

        ret += "\nPyPM Library Versions:\n\n"

        for i in pypmlibs:
            ret += "\t%s - %s\n" % (i, __get_pypm_lib_version(i))

    if git_info:
        info = __get_git_refs(pkginfo_path)

        ret += "\nGit Repository Information:\n\n"
        ret += "\tBranch - %s\n" % __get_git_branch(pkginfo_path)
        ret += "\tHEAD - %s\n" % info.keys()[0]
        ret += "\n\tRefs pointing to HEAD:\n\n"

        for i in info[info.keys()[0]]:
            ret += "\t\t%s" % i
    
    ret += "\n"

    return ret



if __name__ == "__main__":
    print(get_version_info())
    # print(__get_cafe_version(c))
    # libl = __get_pip_lib_list(c)

    # for i in libl:
    #     print("===== %s =====" % i)
    #     print(__get_pip_lib_version(i))


