from dataclasses import dataclass, field
from typing import Optional
try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal

from .priv import PrivConf


@dataclass
class ClsPrivConf(PrivConf):
    """
    Args:
        priv_level (`Literal["1", "2", "3"]`): privacy protection level, where "3" represents the strongest.
        base_budget (`int`, *optional*): If base_budget is 'None', the base budget is determined based on
            the privacy protection level. Otherwise, the base budget is determined by base_budget.
    """
    priv_level: Literal["1", "2", "3"] = field(default="1")
    base_budget: Optional[int] = None
