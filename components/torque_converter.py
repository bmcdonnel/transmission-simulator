class TorqueConverter(object):
  def __init__(self):
    _engine = None
    _transmission = None

  def Initialize(self, model_filename, engine, transmission):
    _engine = engine
    _transmission = transmission

  def GetImpellerTorque(self):
    # TODO finish this
    # engine_speed = _engine.GetEngineSpeed()
    return 0

  def StepOnce(self):
    pass
