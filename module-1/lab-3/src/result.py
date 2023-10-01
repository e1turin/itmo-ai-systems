

class Result():
    def __init__(self, values: tuple[str | bool] | bool | None, format: any) -> None:
        self.values = values
        self.format = format

    def to_string(self) -> str:
        return self.format['answer'](self.values) 
