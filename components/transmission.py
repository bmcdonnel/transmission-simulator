class Transmission(object):
  def __init__(self):
    self._torque_converter = None
    self._vehicle_dynamics = None

    self._gear_ratios = {
      -1 : -2.29,
      0  : 0,
      1  : 3.06,
      2  : 1.63,
      3  : 1.00,
      4  : 0.70
    }

    self._gear = 1
    self._input_speed = 0
    self._output_torque = 0

  def Initialize(self, model_filename, torque_converter, vehicle_dynamics):
    self._torque_converter = torque_converter
    self._vehicle_dynamics = vehicle_dynamics

  def GetGear(self):
    return self._gear

  def GetTransmissionSpeed(self):
    return self._input_speed

  def GetTransmissionTorque(self):
    return self._output_torque

  def StepOnce(self):
    ratio = self._gear_ratios[self._gear]

    self._input_speed = ratio * self._vehicle_dynamics.GetFinalDriveSpeed()
    self._output_torque = ratio * self._torque_converter.GetTurbineTorque()

