class NumberGroup:
  """Process numbers using common mathematical operations.

  This class provides methods to calculate averages, divide numbers,
  generate sequences, and process numbers asynchronously.

  Attributes:
    numbers: A list of numbers to process.
    name: The name of the processor.
  """
  bob = 1

  def __init__(self, numbers: list[float], name: str = 'Default'):
    """Initialize the NumberGroup.

    Args:
      numbers: List of numbers to process.
      name: Name assigned to the processor.
    """
    self.numbers = numbers
    self.name = name

  def calculate_average(self) -> float:
    """Calculate the average of the stored numbers.

    Returns:
      The average of all numbers.

    Raises:
      ValueError: If the numbers list is empty.

    Warnings:
      This method raises an exception rather than returning None
      when no numbers are available.

    References:
      https://docs.python.org/3/library/functions.html#sum

    Examples:
      >>> processor = NumberGroup([10, 20, 30])
      >>> processor.calculate_average()
      20.0
    """
    if not self.numbers:
      raise ValueError('Numbers list cannot be empty')

    return sum(self.numbers) / len(self.numbers)

  def divide(self, a: float, b: float = 1.0) -> float:
    """Divide two numbers.

    Args:
      a: The numerator.
      b: The denominator. Defaults to 1.0.

    Returns:
      The result of the division.

    Raises:
      ZeroDivisionError: If the denominator is zero.

    Warnings:
      A zero denominator will cause a ZeroDivisionError.

    Notes:
      The result is returned as a floating-point number.

    References:
      https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex

    Examples:
      >>> processor = NumberGroup([1, 2])
      >>> processor.divide(10, 2)
      5.0
      >>> processor.divide(10)
      10.0
    """
    return a / b

  def generate_sequence(self, count: int = 5):
    """Generate a sequence of integers.

    Args:
      count: Number of integers to generate. Defaults to 5.

    Yields:
      The next integer in the sequence.

    Raises:
      ValueError: If count is negative.

    Warnings:
      Large values of count may produce long-running iterations.

    References:
      https://docs.python.org/3/library/functions.html#func-range

    Examples:
      >>> processor = NumberGroup([])
      >>> list(processor.generate_sequence(3))
      [0, 1, 2]
    """
    if count < 0:
      raise ValueError('Count cannot be negative')

    yield from range(count)

  async def calculate_average_async(self) -> float:
    """Calculate the average asynchronously.

    Returns:
      The average of all stored numbers.

    Raises:
      ValueError: If the numbers list is empty.

    Warnings:
      This method does not perform asynchronous I/O or yield control
      to other tasks because its current implementation is synchronous
      internally.

    References:
      https://docs.python.org/3/library/asyncio.html

    Examples:
      >>> processor = NumberGroup([10, 20, 30])
      >>> await processor.calculate_average_async()
      20.0
    """
    if not self.numbers:
      raise ValueError('Numbers list cannot be empty')

    return sum(self.numbers) / len(self.numbers)

  @classmethod
  def from_string(cls, values: str, name: str = 'Parsed') -> NumberGroup:
    """Create a NumberGroup from a comma-separated string.

    Args:
      values: Comma-separated numeric values.
      name: Name assigned to the processor. Defaults to "Parsed".

    Returns:
      A new NumberGroup instance.

    Raises:
      ValueError: If any value cannot be converted to a float.

    Warnings:
      Empty values or malformed numeric strings will cause conversion
      to fail.

    References:
      https://docs.python.org/3/library/stdtypes.html#str.split
      https://docs.python.org/3/library/functions.html#float

    Examples:
      >>> processor = NumberGroup.from_string("10,20,30")
      >>> processor.numbers
      [10.0, 20.0, 30.0]
    """
    numbers = [float(value.strip()) for value in values.split(',')]
    return cls(numbers, name)
