from typing import List, Optional, overload, Unpack

from . import Rule, Config

class Pos:
    line: int
    column: int
    index: int

class Range:
    start: Pos
    end: Pos

class SgRoot:
    def __init__(self, src: str, language: str) -> None: ...
    def root(self) -> SgNode: ...
    def filename(self) -> str: ...

class SgNode:
    # Node Inspection
    def range(self) -> Range: ...
    def is_leaf(self) -> bool: ...
    def is_named(self) -> bool: ...
    def is_named_leaf(self) -> bool: ...
    def kind(self) -> str: ...
    def text(self) -> str: ...

    # Refinement
    def matches(self, **rule: Unpack[Rule]) -> bool: ...
    def inside(self, **rule: Unpack[Rule]) -> bool: ...
    def has(self, **rule: Unpack[Rule]) -> bool: ...
    def precedes(self, **rule: Unpack[Rule]) -> bool: ...
    def follows(self, **rule: Unpack[Rule]) -> bool: ...
    def get_match(self, meta_var: str) -> Optional[SgNode]: ...
    def get_multiple_matches(self, meta_var: str) -> List[SgNode]: ...
    def get_transformed(self, meta_var: str) -> Optional[str]: ...
    def __getitem__(self, meta_var: str) -> SgNode: ...

    # Search
    @overload
    def find(self, config: Config) -> Optional[SgNode]: ...
    @overload
    def find(self, **kwargs: Unpack[Rule]) -> Optional[SgNode]: ...
    @overload
    def find_all(self, config: Config) -> List[SgNode]: ...
    @overload
    def find_all(self, **kwargs: Unpack[Rule]) -> List[SgNode]: ...

    # Tree Traversal
    def get_root(self) -> SgRoot: ...
    def field(self, name: str) -> Optional[SgNode]: ...
    def parent(self) -> Optional[SgNode]: ...
    def child(self, nth: int) -> Optional[SgNode]: ...
    def children(self) -> List[SgNode]: ...
    def ancestors(self) -> List[SgNode]: ...
    def next(self) -> Optional[SgNode]: ...
    def next_all(self) -> List[SgNode]: ...
    def prev(self) -> Optional[SgNode]: ...
    def prev_all(self) -> List[SgNode]: ...