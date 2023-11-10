from typing import List

from CollectorHBA import CollectorHBA
from SmartMeterHBA import SmartMeterHBA


class VirtualCollectorHBA:
    def __init__(
        self,
        collectors: List[CollectorHBA],
        sm_sample: List[SmartMeterHBA],
        count_sm_per_col: List[int],
        sm_belongs_to_col_of_index: List[int]
    ):
        self.collectors = collectors
        self.sm_sample = sm_sample
        self.count_sm_per_col = count_sm_per_col
        self.sm_belongs_to_col_of_index = sm_belongs_to_col_of_index