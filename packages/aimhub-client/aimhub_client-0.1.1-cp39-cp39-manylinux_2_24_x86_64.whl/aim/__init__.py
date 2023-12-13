import aimrocks # noqa

from aim._sdk.base.record import Record
from aim._sdk.base.sequence import Sequence
from aim._sdk.base.container import Container, Property
from aim._sdk.base.repo import Repo
from aim._sdk.types.run import Run
from aim._sdk.types.metric import Metric, SystemMetric
from aim._ext.notebook.notebook import load_ipython_extension
from aim._ext.analytics import analytics

__all__ = ['Record', 'Sequence', 'Container', 'Repo', 'Property', 'Run', 'Metric', 'SystemMetric']

analytics.track_install_event()
