from typing import List

from spidermon import Monitor, MonitorSuite
from spidermon.contrib.actions.telegram.notifiers import SendTelegramMessageSpiderFinished
from spidermon.contrib.monitors.mixins import StatsMonitorMixin
from spidermon.contrib.scrapy.monitors import SpiderCloseMonitorSuite, ErrorCountMonitor, FinishReasonMonitor, \
    UnwantedHTTPCodesMonitor
from spidermon.decorators import monitors


# @monitors.name('LiveScience Item Validation Monitor')
# class LiveScienceItemValidateMonitor(Monitor, StatsMonitorMixin):
#
#     @monitors.name('Should not have any missing fields')
#     def test_item_structure_validation(self):
#         validation_errors = getattr(
#             self.stats, 'spidermon/validation/fields/errors', 0
#         )
#         self.assertEqual(
#             validation_errors,
#             0,
#             msg='Found validation errors in {} fields'.format(
#                 validation_errors)
#         )


class NewsCrawlerSpiderCloseMonitorSuite(MonitorSuite):
    monitors: List = [
        ErrorCountMonitor,
        FinishReasonMonitor,
        UnwantedHTTPCodesMonitor,
    ]
    monitors_finished_actions = [
        SendTelegramMessageSpiderFinished
    ]
    monitors_failed_actions = [
        # SendTelegramMessageSpiderFinished
        #SendSentryMessage
    ]


# class LiveScienceCloseMonitorSuite(NewsCrawlerSpiderCloseMonitorSuite):
#     monitors = NewsCrawlerSpiderCloseMonitorSuite.monitors + [
#         LiveScienceItemValidateMonitor,
#     ]
