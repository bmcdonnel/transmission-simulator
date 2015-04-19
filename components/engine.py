class Engine(object):
  def __init__(self):
    self._torque_converter = None

    self._engine_speed = 0
    self._engine_impeller_moment = 1

  def Initialize(self, engine_model_filename, torque_converter):
    self._engine_model = self._LoadEngineModelFromFile(engine_model_filename)
    self._torque_converter = torque_converter

  def StepOnce(self, throttle_position):
    engine_torque = self._GetEngineTorque(throttle_position, self._engine_speed)
    impeller_torque = self._torque_converter.GetImpellerTorque()

    print "impeller torque: " + str(impeller_torque)
    # TODO integrate this?
    self._engine_speed = (engine_torque - impeller_torque) / self._engine_impeller_moment

    # engine can't rev higher than 5000 RPM
    if self._engine_speed > 5000:
      self._engine_speed = 5000

    self._torque_converter.StepOnce()

  def GetEngineSpeed(self):
    return self._engine_speed

  def _GetEngineTorque(self, throttle_position, rpm):
    # TODO look up torque in engine model map loaded from file
    # return self._engine_model[throttle_position][rpm]
    return 1

  def _LoadEngineModelFromFile(self, filename):
    model = dict()

    with open(filename) as f:
      # TODO finish this
      pass

    return model
