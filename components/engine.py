class Engine(object):
  def __init__(self, torque_converter):
    _torque_converter = torque_converter
    _current_RPM = 0
    _engine_impeller_moment = 0
    _torque_curve = dict()

  def ComputeNextEngineSpeed(self, throttle_position):
    engine_torque = _getEngineTorque(throttle_position, self._current_RPM)
    impeller_torque = _torque_converter.GetImpellerTorque()
    return 

  def GetCurrentEngineSpeed(self):
    return _current_RPM

  def _getEngineTorque(self, throttle_position, rpm):
    #TODO look up torque in engine model map loaded from file
    # return _torque_curve[throttle_position][rpm]
    return 0
