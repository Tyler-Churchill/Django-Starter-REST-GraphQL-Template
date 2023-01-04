# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot

snapshots = Snapshot()

snapshots["PublicProductPerformanceTest::test__list__querycount 1"] = {
    "total_queries": 2
}
