import logging
import math

class VehicleDynamics(object):
  def __init__(self):
    self._transmission = None

    self._friction_coefficient = 0.015
    self._drag_coefficient = 0.30 # typical for a modern SUV
    self._final_drive_ratio = 4.10
    self._input_speed = 0
    self._brake_torque = 6000

    # TODO units and order of magnitude
    self._vehicle_load = 1000
    self._vehicle_inertia = 1
    self._wheel_speed = 1              # RPM
    self._wheel_radius = 1             # feet
    self._vehicle_linear_velocity = 0  # MPH

  def Initialize(self, transmission):
    self._transmission = transmission

  def GetFinalDriveSpeed(self):
    return self._input_speed

  def GetVehicleSpeed(self):
    return self._vehicle_linear_velocity

  def SetBrakeTorque(self, brake_torque):
    self._brake_torque = brake_torque
    self.StepOnce()

  def StepOnce(self):
    sum_of_torques = (self._transmission.GetTransmissionTorque() * self._final_drive_ratio) - self._vehicle_load

    logging.info("(transmission_torque * final_drive_ratio) - vehicle_load = ({} * {}) - {} = {}".format(self._transmission.GetTransmissionTorque(), self._final_drive_ratio, self._vehicle_load, sum_of_torques))

    # TODO what about when speed is 0
    self._input_speed = max(0, sum_of_torques) / self._vehicle_inertia

    """
    if self._wheel_speed != 0:
      self._input_speed /= self._wheel_speed
    """

    self._vehicle_load = ((self._friction_coefficient) +
                          (self._drag_coefficient * self._vehicle_linear_velocity * self._vehicle_linear_velocity) +
                          (self._brake_torque))
    # self._vehicle_load *= math.fabs(self._vehicle_linear_velocity) # is this needed

    logging.info("final drive speed {}, vehicle load {}".format(self._input_speed, self._vehicle_load))

