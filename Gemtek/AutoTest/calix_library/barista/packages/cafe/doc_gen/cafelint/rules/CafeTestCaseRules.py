from rflint.common import TestRule, ERROR


class CafeTestCaseCheckDocumentation(TestRule):
    """
    Verify that loop steps in test case should be less than configured max steps.
    """
    severity = ERROR

    def apply(self, testcase):
        if testcase.is_templated:
            return

        for setting in testcase.settings:
            if setting[1].lower() == "[documentation]" and len(setting) > 2:
                return

        self.report(testcase, '%s: no ducumentation, Test Case: %s' % (self.name, testcase.name), testcase.linenumber)


class CafeTestCaseCheckLoopSteps(TestRule):
    """
    Verify that loop steps in test case should be less than configured max steps.
    """
    severity = ERROR
    max_steps = 10
    details = False

    def configure(self, max_steps=10, details=False):
        self.max_steps = int(max_steps)
        if isinstance(details, bool):
            self.details = details
        elif isinstance(details, str):
            self.details = True if details == 'True' else False
        else:
            self.details = False

    def apply(self, testcase):
        if testcase.is_templated:
            return

        startline = 0
        is_loop = False
        count = 0
        loop_str = ''
        steps = [step for step in testcase.steps if (len(step) > 1 or step[0])]
        for step in steps:
            step_str = '    '.join(step).strip()
            if not is_loop:
                if 'FOR' in step_str and 'IN' in step_str:
                    is_loop = True
                    startline = step.startline
                    loop_str += '%s:\t%s\n' % (count, step_str)
            else:
                if '\\' in step_str:
                    count += 1
                    loop_str += '%s:\t%s\n' % (count, step_str)
                else:
                    if count > self.max_steps:
                        self.report(testcase, '%s: loop steps(%s) should be less than %s, Test Case: %s'
                                    % (self.name, count, self.max_steps, testcase.name),
                                    startline)
                        if self.details:
                            print loop_str
                    is_loop = False
                    count = 0
                    loop_str = ''


class CafeTestCaseCheckCommentLines(TestRule):
    """
    Verify that loop steps in test case should be less than configured max steps.
    Below statement will be treated as comment:
    1) # this is a comment
    2) Comment    use comment keyword to comment
    3) Log To Console    use Log/Log Many/Log To Console to log
    """

    def apply(self, testcase):
        steps = [step for step in testcase.steps if (len(step) > 1 or step[0])]
        total_count = len(steps)
        comment_count = 0
        for step in steps:
            step_str = ' '.join(step).lower().strip(' \\')
            if 'comment' in step_str or step_str.startswith('log'):
                comment_count += 1

        count = 0
        for statement in testcase.statements:
            if ''.join(statement).startswith('#'):
                count += 1

        total_count += count
        comment_count += count
        self.report(testcase, '%s: total(%s), comments(%s), Test Case: %s'
                    % (self.name, total_count, comment_count, testcase.name),
                    testcase.linenumber)


class CafeTestCaseCheckSleep(TestRule):
    """
    Verify that test case should not use sleep, except there are comments
    """
    severity = ERROR

    def apply(self, testcase):
        last_step = None
        for step in testcase.steps:
            step_str = '    '.join(step).strip().lower()
            last_step_str = '    '.join(last_step).strip().lower() if last_step else ''
            if step_str.startswith('sleep') or step_str.startswith('\\    sleep'):
                if ('comment' not in last_step_str) and ('log' not in last_step_str):
                    self.report(testcase, '%s: (%s), Test Case: %s'
                                % (self.name, '    '.join(step).strip(),
                                   testcase.name), step.startline)

            last_step = step
