from rflint.common import KeywordRule, ERROR


class CafeKeywordCheckDocumentation(KeywordRule):
    """
    Verify that keyword must have documentation
    """
    severity = ERROR

    def apply(self, keyword):
        for setting in keyword.settings:
            if setting[1].lower() == "[documentation]" and len(setting) > 2:
                return

        self.report(keyword, '%s: no ducumentation, Keyword: %s' % (self.name, keyword.name), keyword.linenumber)


class CafeKeywordCheckSleep(KeywordRule):
    """
    Verify that keyword should not use sleep, except there are comments
    """
    severity = ERROR

    def apply(self, keyword):
        last_step = None
        for step in keyword.steps:
            step_str = '    '.join(step).strip().lower()
            last_step_str = '    '.join(last_step).strip().lower() if last_step else ''
            if step_str.startswith('sleep') or step_str.startswith('\\    sleep'):
                if ('comment' not in last_step_str) and ('log' not in last_step_str):
                    self.report(keyword, '%s: (%s), Keyword: %s'
                                % (self.name, '    '.join(step).strip(),
                                   keyword.name), step.startline)

            last_step = step
