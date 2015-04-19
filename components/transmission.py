class Transmission(object):
  def __init__(self):
    _torque_converter = None
    _vehicle_dynamics = None

  def Initialize(self, model_filename, torque_converter, vehicle_dynamics):
    _torque_converter = torque_converter
    _vehicle_dynamics = vehicle_dynamics

  def StepOnce(self):
    pass
