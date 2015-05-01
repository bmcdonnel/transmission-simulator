import logging
import math

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
    engine_torque = self._engine.GetEngineTorque()
    engine_speed = self._engine.GetEngineSpeed()
    transmission_speed = self._transmission.GetTransmissionSpeed()
    transmission_torque = self._transmission.GetTransmissionTorque()

    speed_ratio = transmission_speed / float(engine_speed)

    torque_ratio = transmission_torque / float(engine_torque)
    capacity = self._Capacity(engine_speed, engine_torque, speed_ratio)

    logging.info("turbine-speed:impeller-speed = {}:{} = {}".format(transmission_speed, engine_speed, speed_ratio))

    self._impeller_torque = self._Sign(1 - speed_ratio) * math.pow(engine_speed / capacity, 2)
    self._turbine_torque = self._impeller_torque * torque_ratio

    logging.info("(impeller_torque, turbine_torque) = ({}, {})".format(self._impeller_torque,
                                                                       self._turbine_torque))
    self._transmission.StepOnce()

  def _Capacity(self, engine_speed, engine_torque, speed_ratio):
    if speed_ratio < 1.0:
      return engine_speed / math.sqrt(engine_torque)
    else:
      return engine_speed

  def _Sign(self, value):
    if value < 0:
      return -1
    elif value == 0:
      return 0
    elif value > 0:
      return 1

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

