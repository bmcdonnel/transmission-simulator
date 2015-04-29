import logging

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

    transmission_speed = self._transmission.GetTransmissionSpeed()
    engine_speed = self._engine.GetEngineSpeed()
    speed_ratio = transmission_speed / engine_speed
    torque_multiplier = self._TorqueTransferMultiplier(speed_ratio)
    transfer_coefficient = self._TurbineTransferCoefficient(speed_ratio)

    logging.info("turbine-speed:impeller-speed = {}:{} = {}".format(transmission_speed, engine_speed, speed_ratio))

    self._turbine_torque = torque_multiplier * transfer_coefficient * self._impeller_torque
    logging.info("multiplier * coefficient * impeller_torque = {} * {} * {} = {}".format(torque_multiplier,
                                                                                         transfer_coefficient,
                                                                                         self._impeller_torque,
                                                                                         self._turbine_torque))

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

  def _TorqueTransferMultiplier(self, speed_ratio):
    # multiply torque when the turbine is spinning up
    if speed_ratio < 0.10:
      return 2
    elif speed_ratio < 0.20:
      return 1.75
    elif speed_ratio < 0.30:
      return 1.25
    else:
      return 1

  def _TurbineTransferCoefficient(self, speed_ratio):
    # 100% transfer when the turbine is stalled
    # tapers off linearly as the speeds match
    return (10 - speed_ratio) / 10

