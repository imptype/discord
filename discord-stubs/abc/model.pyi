from typing import Any

def snowflake_time(id) -> Any: # TODO
  """
  TODO

  Args:
    id: TODO

  Returns:
    TODO
  """

class Snowflake:
  """
  TODO

  Attributes:
    id: TODO
    created_at: TODO
  """

  id: Any # TODO
  created_at: Any # TODO

  def __init__(self, id) -> None: # TODO
    """
    TODO

    Args:
      id: TODO
    """

class PartialModel(Snowflake):
  """
  TODO

  Attributes:
    app: TODO
  """

  app: Any # TODO

  def __init__(self, app, id) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      id: TODO
    """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """
