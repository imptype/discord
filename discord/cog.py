"""
cog.py - inherit this class and override methods to do stuff.
"""

class Cog:
  def __init__(self, app):
    self.app = app

  async def cog_load(self):
    pass
