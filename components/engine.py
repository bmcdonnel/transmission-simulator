class Engine(object):
  def __init__(self):
    _torque_converter = None
    _engine_speed = 0
    _engine_impeller_moment = 1

  def Initialize(self, engine_model_filename, torque_converter):
    _engine_model = self._LoadEngineModelFromFile(engine_model_filename)
    _torque_converter = torque_converter

  def StepOnce(self, throttle_position):
    engine_torque = _GetEngineTorque(throttle_position, _engine_speed)
    impeller_torque = _torque_converter.GetImpellerTorque()

    # TODO integrate this?
    _engine_speed = (engine_torque - impeller_torque) / _engine_impeller_moment

  def GetEngineSpeed(self):
    return _current_RPM

  def _GetEngineTorque(self, throttle_position, rpm):
    # TODO look up torque in engine model map loaded from file
    # return _engine_model[throttle_position][rpm]
    return 0

  def _LoadEngineModelFromFile(self, filename):
    model = dict()

    with open(filename) as f:
      # TODO finish this
      pass

    return model
