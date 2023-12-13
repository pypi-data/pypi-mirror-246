from .chip_model import *
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .ChipError import ChipError
    from .InternalState import InternalState
    from freq_allocator.stubs import FreqAllocatorCpp

def single_err_model(chip : ChipError) -> Tuple[float, InternalState]:
    return FreqAllocatorCpp.single_err_model(chip)

def loss(frequencies : List[float]) -> float:
    return FreqAllocatorCpp.loss(frequencies)

def random_loss() -> float:
    return FreqAllocatorCpp.random_loss()

def random_allow_freq_loss() -> float:    
    return FreqAllocatorCpp.random_allow_freq_loss()
