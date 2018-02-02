#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pkg_resources
import sys

__author__ = 'David Qian'

"""
Created on 06/14/2016
@author: David Qian

"""


def get_pkg_license(pkgname):
    """
    Given a package reference (as from requirements.txt),
    return license listed in package metadata.
    NOTE: This function does no error checking and is for
    demonstration purposes only.
    """
    pkgs = pkg_resources.require(pkgname)
    pkg = pkgs[0]
    if not pkg.has_metadata('PKG-INFO'):
        return None
    for line in pkg.get_metadata_lines('PKG-INFO'):
        (k, v) = line.split(': ', 1)
        if k == "License":
            return v
    return None


def get_pkgs_license(pkgs):
    ret = []
    for pkg in pkgs:
        pkg = pkg.split('>')[0]
        _license = get_pkg_license(pkg)
        if not _license:
            _license = 'UNKNOWN'

        ret.append((pkg, _license))

    return ret


if __name__ == '__main__':
    args = []
    for arg in sys.argv[1:]:
        args.extend(arg.split())

    ret = get_pkgs_license(args)
    for k, v in ret:
        print '%s | %s' % (k, v)
