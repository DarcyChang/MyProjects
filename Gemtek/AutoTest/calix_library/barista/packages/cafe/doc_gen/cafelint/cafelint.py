from __future__ import print_function
import sys
import os
import glob
from pprint import pprint
import argparse

import yaml
try:
    from rflint import RfLint as lint
except ImportError:
    lint = None

SEVERITY = ('ignore', 'error', 'warning')


class CafeLint(object):
    def __init__(self, args):
        parser = argparse.ArgumentParser(description='Cafelint: robot code check tool')
        parser.add_argument('--config', help='Cafelint config file')
        _args = parser.parse_args(args)

        self.args = ['--recursive', '--ignore', 'all']
        self.maps = None
        self.config = _args.config
        self.load_config_yaml_file()

    @property
    def format(self):
        return self.maps.get('format', '') if self.maps else ''

    @property
    def target(self):
        return self.maps.get('target', []) if self.maps else []

    @property
    def debug(self):
        return self.maps.get('debug', False) if self.maps else False

    @staticmethod
    def _get_path(path):
        return os.path.abspath(os.path.expanduser(path))

    def _add_argument(self, argument, value):
        self.args.extend(['--' + argument, value])

    def _add_rule(self, rule, severity):
        rules = rule.get(severity, None)
        if rules:
            for rule in rules:
                self._add_argument(severity, rule)

    def load_config_yaml_file(self):
        self.config = self._get_path(self.config)
        if not os.path.exists(self.config):
            print('Can not find config file: %s' % self.config)
            return

        self.maps = yaml.load(file(self.config))

        rules = self.maps.get('rules', None)
        if not rules:
            return

        directory = rules.get('directory', None)
        if not directory:
            return

        for d in directory:
            for filename in glob.glob(self._get_path(d) + '/*.py'):
                if filename.endswith('__init__.py'):
                    continue
                else:
                    self._add_argument('rulefile', filename)

        rule = rules.get('rule', None)
        if rule:
            for s in SEVERITY:
                self._add_rule(rule, s)

            for option in rule.keys():
                if option not in SEVERITY:
                    detailed_rule = rule[option]
                    for key in detailed_rule:
                        if key in 'severity':
                            self._add_argument(detailed_rule[key], option)
                        elif key in 'configure':
                            self._add_argument(key, option + ':' + detailed_rule[key])
                        else:
                            print('wrong option')

        if self.format:
            self._add_argument('format', self.format)

        if not self.target:
            print('There is no target in config file')
            return
        else:
            for d in self.target:
                self.args.append(self._get_path(d))

        if self.debug:
            pprint(self.args)

    def run(self):
        if lint:
            return lint().run(self.args)


def main(args=None):
    if not lint:
        command = 'sudo /opt/ActivePython-2.7/bin/pip install --upgrade robotframework-lint'
        print('No robotframework-rflint library, please use this command `%s` to install.' % command)
        return 1

    try:
        CafeLint(args).run()
    except Exception, e:
        sys.stderr.write(str(e) + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
