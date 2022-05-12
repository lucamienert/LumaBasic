class Error:
    def __init__(self, pos_start, pos_end, error_name, details) -> None:
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def error_as_string(self):
        return f'{self.error_name}: {self.details}\n' 