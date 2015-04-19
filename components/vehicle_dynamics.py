class VehicleDynamics(object):
  def __init__(self):
    self._transmission = None

    self._final_drive_ratio = 4.10
    self._input_speed = 0

    # TODO units and order of magnitude
    self._vehicle_load = 1000
    self._vehicle_inertia = 1
    self._wheel_speed = 1      # RPM
    self._wheel_radius = 1     # feet
    self._vehicle_linear_velocity = 0       # MPH

  def Initialize(self, transmission):
    self._transmission = transmission

  def GetFinalDriveSpeed(self):
    return self._input_speed

  def GetVehicleSpeed(self):
    return self._vehicle_linear_velocity

  def StepOnce(self):
    # TODO what about when speed is 0
    self._input_speed = self._transmission.GetTransmissionTorque() * self._final_drive_ratio - self._vehicle_load
    self._input_speed /= self._vehicle_inertia
    self._input_speed /= self._wheel_speed

    self._vehicle_load = (self._friction_coefficient +
                          self._drag_coefficient * self._vehicle_linear_velocity * self._vehicle_linear_velocity +
                          self._brake_torque)
    self._vehicle_load *= self._vehicle_linear_velocity
