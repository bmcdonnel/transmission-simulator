class TorqueConverter(object):
  def __init__(self):
    self_engine = None
    self._transmission = None

    self._impeller_torque = 0
    self._turbine_torque = 0

  def Initialize(self, model_filename, engine, transmission):
    self._engine = engine
    self._transmission = transmission

  def GetImpellerTorque(self):
    return self._impeller_torque

  def GetTurbineTorque(self):
    return self._turbine_torque

  def StepOnce(self):
    self._impeller_torque = self._engine.GetEngineTorque()

    """
    # TODO these equations aren't quite right
    impeller_speed = self._engine.GetEngineSpeed()
    turbine_speed = self._transmission.GetTransmissionSpeed()
    speed_ratio = 1

    if turbine_speed != 0 and impeller_speed != 0:
      # TODO add a lossy transfer function
      speed_ratio = turbine_speed / impeller_speed

    self._impeller_torque = impeller_speed / speed_ratio
    self._impeller_torque *= self._impeller_torque
    self._turbine_torque = self._impeller_torque
    """

    self._transmission.StepOnce()

