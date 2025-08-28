from typing import TextIO, Tuple


class InputStream:
    def __init__(self, file: TextIO) -> None:
        file.seek(0)
        self.file: TextIO = file
        self.line: int = 1
        self.column: int = 0
        self.current: str = self.file.read(1)

    def peek(self) -> str:
        return self.current

    def advance(self) -> str:
        if self.current == "\n":
            self.line += 1
            self.column = 0
        else:
            self.column += 1
        self.current = self.file.read(1)
        return self.current

    def eof(self) -> bool:
        return self.current == ""

    def position(self) -> Tuple[int, int]:
        return self.line, self.column
