from __future__ import absolute_import, division, print_function

from oct.tests.unit.playbook_runner_test_case import PlaybookRunnerTestCase, TestCaseParameters, show_stack_trace
from oct.util.playbook import playbook_path

if not show_stack_trace:
    __unittest = True


class BootstrapHostTestCase(PlaybookRunnerTestCase):
    def test_boostrap_host(self):
        self.run_test(
            TestCaseParameters(
                args=['bootstrap', 'host'],
                expected_calls=[{
                    'playbook_source': playbook_path('bootstrap/host'),
                    'playbook_variables': None
                }]
            )
        )
