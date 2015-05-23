import logging
import utilities.map_loader

class Engine(object):
  def __init__(self):
    self._torque_converter = None

    self._torque_map = dict()
    self._engine_max_speed = 0
    self._engine_speed = 0
    self._engine_torque = 0
    self._engine_impeller_moment = 0.02 # 10 inch torque converter

    self._engine_speed_steps = []
    self._torque_steps = []

  def Initialize(self, torque_map_filename, torque_converter):
    logging.info("Inititalizing Engine from " + torque_map_filename)

    self._LoadTorqueMapFromFile(torque_map_filename)
    self._torque_converter = torque_converter

  def Start(self):
    self._engine_speed = 800
    self._engine_torque = self._GetEngineTorque(0, self._engine_speed)
    self._torque_converter.StepOnce()

    logging.info("Engine started; idling at " + str(self._engine_speed) + " RPM")

  def StepOnce(self, throttle_position):
    self._engine_torque = self._GetEngineTorque(throttle_position, self._engine_speed)
    impeller_torque = self._torque_converter.GetImpellerTorque()

    logging.info("engine (speed, torque) = ({}, {}), impeller torque {}".format(self._engine_speed, self._engine_torque, impeller_torque))

    # TODO integrate this?
    self._engine_speed += int((self._engine_torque - impeller_torque) * self._engine_impeller_moment)

    logging.info("new engine speed {}".format(self._engine_speed))

    if self._engine_speed > self._engine_max_speed:
      logging.info("rev limiting engine to {}".format(self._engine_max_speed))
      self._engine_speed = self._engine_max_speed

    self._engine_speed_steps.append(self._engine_speed)
    self._torque_steps.append(self._engine_torque)

    self._torque_converter.StepOnce()

  def GetEngineSpeed(self):
    return self._engine_speed

  def GetEngineSpeedSteps(self):
    return self._engine_speed_steps

  def GetEngineTorque(self):
    return self._engine_torque

  def GetTorqueSteps(self):
    return self._torque_steps

  def GetTorqueMap(self):
    return self._torque_map

  def _GetEngineTorque(self, throttle_position, rpm):
    return self._torque_map[throttle_position][rpm]

  def _LoadTorqueMapFromFile(self, filename):

    mapLoader = utilities.map_loader.MapLoader(filename)

    self._torque_map, value_count = mapLoader.LinearlyInterpolate()

    self._engine_max_speed = self._torque_map[0].keys()[-1]

    logging.info("Loaded " + str(value_count) + " torque values")
    logging.info("Max engine RPM " + str(self._engine_max_speed))

