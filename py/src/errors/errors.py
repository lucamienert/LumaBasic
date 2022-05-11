from error import Error

class IllegalCharError(Error):
  def __init__(self, pos_start, pos_end, details) -> None:
    super().__init__(pos_start, pos_end, 'Illegal Character', details)

class ExpectedCharError(Error):
  def __init__(self, pos_start, pos_end, details) -> None:
    super().__init__(pos_start, pos_end, 'Expected Character', details)

class InvalidSyntaxError(Error):
  def __init__(self, pos_start, pos_end, details='') -> None:
    super().__init__(pos_start, pos_end, 'Invalid Syntax', details)

class RTError(Error):
  def __init__(self, pos_start, pos_end, details, context) -> None:
    super().__init__(pos_start, pos_end, 'Runtime Error', details)
    self.context = context