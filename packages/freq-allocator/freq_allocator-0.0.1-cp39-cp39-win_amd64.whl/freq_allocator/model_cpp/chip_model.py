import FreqAllocatorCpp
from pathlib import Path
from typing import List, TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from .ChipError import ChipError
    from .ChipNode import ChipNode
    from .InternalState import InternalState
else:
    class ChipError:...
    class ChipNode:...
    class InternalState:...

class ChipModel:    
    def __init__(self, basepath):
        self.inst = FreqAllocatorCpp.SingleErrorAllocation.get_instance()
        self.chip.load_file(
            str(Path(basepath) / 'qubit_data.json'), 
            str(Path(basepath) / 'xy_crosstalk_sim.json'))
    
    @property
    def H(self) -> int:
        return self.inst.H

    @property
    def W(self) -> int:
        return self.inst.W
    
    @property
    def chip(self) -> ChipError:
        return self.inst.chip
    
    @property
    def n_available_nodes(self) -> int:
        return self.get_n_available_nodes()
    
    @property
    def allocated(self) -> List[Tuple[int, int]]:
        return self.list_all_allocated()
        
    @property
    def unallocated(self) -> List[Tuple[int, int]]:
        return self.list_all_allocated()
    
    def get_nodes(self) -> List[ChipNode]:    
        return self.chip.nodes
            
    def get_n_available_nodes(self) -> int:
        return self.chip.n_available_nodes
    
    def qubit_name_idx(self, x : int, y : int) -> int:
        return self.chip.qubit_name_idx(x, y)
    
    def qubit_idx(self, x : int, y : int) -> int:
        return self.chip.qubit_idx(x, y)
    
    def check_available_pair(self, x : int, y : int) -> bool:
        return self.chip.check_available_pair(x, y)
    
    def get_neighbors(self, x, y) -> List[Tuple[int, int]]:
        return self.chip.get_neighbors(x, y)
        
    def get_neighbors_distance_sqrt2(self, x, y) -> List[Tuple[int, int]]:
        return self.chip.get_neighbors_distance_sqrt2(x, y)
        
    def get_neighbors_distance_2(self, x, y) -> List[Tuple[int, int]]:
        return self.chip.get_neighbors_distance_2(x, y)
        
    def initialize_all_nodes(self) -> None:
        return self.chip.initialize_all_nodes()
    
    def list_all_unallocated(self) -> List[Tuple[int, int]]:
        return self.chip.list_all_unallocated()
    
    def list_all_allocated(self) -> List[Tuple[int, int]]:
        return self.chip.list_all_allocated()
    
    def assign_frequencies(self, frequencies) -> None:
        return self.chip.assign_frequencies(frequencies)
    
    def list_freq_ranges(self) -> List[Tuple[float, float]]:
        return self.chip.list_freq_ranges()

