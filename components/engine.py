import logging

class Engine(object):
  def __init__(self):
    self._torque_converter = None

    self._torque_map = dict()
    self._engine_speed = 0
    self._engine_torque = 0
    self._engine_impeller_moment = 0.02 # 10 inch torque converter

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

    logging.info("engine torque {}, impeller torque {}".format(self._engine_torque, impeller_torque))

    # TODO integrate this?
    self._engine_speed += int((self._engine_torque - impeller_torque) * self._engine_impeller_moment)

    logging.info("engine speed {}".format(self._engine_speed))

    # engine can't rev higher than 5000 RPM
    if self._engine_speed > 5000:
      self._engine_speed = 5000

    self._torque_converter.StepOnce()

  def GetEngineSpeed(self):
    return self._engine_speed

  def GetEngineTorque(self):
    return self._engine_torque

  def _GetEngineTorque(self, throttle_position, rpm):
    return self._torque_map[throttle_position][rpm]

  def _LoadTorqueMapFromFile(self, filename):
    total_torque_values = 0

    with open(filename) as f:
      # drop the first item of the first line since its just a
      # spacer representing the throttle position column
      rpm_values = f.readline().split()[1:]

      logging.info(str(len(rpm_values)) + " RPM values")

      # count the rest of the lines remaining in the file (excluding the first line of RPM values)
      throttle_position_count = sum(1 for line in f)

      logging.info(str(throttle_position_count) + " throttle position values")

      # seek back to the second line to start loading torque values
      f.seek(0)
      f.readline()

      for line in f:
        # split off the first value representing the throttle position
        throttle_position = int(line.split(' ', 1)[0])

        if throttle_position not in self._torque_map:
          self._torque_map[throttle_position] = dict()

        # the rest are torque values for each RPM at that throttle position
        torque_values = line.split()[1:]

        if len(torque_values) != len(rpm_values):
          raise Exception('Each RPM must have a torque value for throttle position ' + str(throttle_position))

        for i in range(len(rpm_values) - 1):
          # grab two rpm values
          rpm_a = int(rpm_values[i])
          rpm_b = int(rpm_values[i + 1])
          rpm_diff = rpm_b - rpm_a

          # grab the two associated torque values
          torque_a = int(torque_values[i])
          torque_b = int(torque_values[i + 1])
          torque_diff = torque_b - torque_a

          # force floating point division
          ratio = torque_diff / float(rpm_diff)

          for j in range(rpm_diff):
            rpm = rpm_a + j
            torque = int(torque_a + (ratio * j))

            if torque < 0:
              raise Exception('negative torque {} for rpm {} resulting from rpm({}, {}), torque({}, {}), ratio {} at throttle {}'.format(torque, rpm, rpm_a, rpm_b, torque_a, torque_b, ratio, throttle_position))

            self._torque_map[throttle_position][rpm] = torque
            total_torque_values += 1

    logging.info("Loaded " + str(total_torque_values) + " torque values")

