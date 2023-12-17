from .chip_model import *
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .ChipError import ChipError
    from .InternalState import InternalState
    from freq_allocator.stubs import FreqAllocatorCpp

def single_err_model(chip : ChipError, record_internal_state : bool = False) -> Tuple[float, InternalState]:
    return FreqAllocatorCpp.single_err_model(chip, record_internal_state)

def loss(frequencies : List[float]) -> float:
    return FreqAllocatorCpp.loss(frequencies)

def loss_on_range(ranges : List[float]) -> float:
    return FreqAllocatorCpp.loss_on_range(ranges)

def random_loss() -> float:
    return FreqAllocatorCpp.random_loss()

def random_allow_freq_loss() -> float:    
    return FreqAllocatorCpp.random_allow_freq_loss()
