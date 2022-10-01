from typing import TypeAlias, Callable

Position: TypeAlias = int
Coordinate: TypeAlias = tuple[Position, Position]

Head: TypeAlias = Coordinate
Tail: TypeAlias = list[Coordinate]
Snake: TypeAlias = (Head, Tail)

Pellet: TypeAlias = Coordinate
Direction = Callable[[Coordinate], Coordinate]
