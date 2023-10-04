
class Query():
    def __init__(self, format: any, params: tuple[str]) -> None:
        self.format = format
        self.params: tuple[str] = params

    def to_string(self) -> str:
        return self.format['query'].format(*self.params)
