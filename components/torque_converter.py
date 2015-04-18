class TorqueConverter(object):
  def __init__(self, engine):
    _engine = engine

  def GetImpellerTorque(self):
    return _engine.GetCurrentEngineSpeed()
