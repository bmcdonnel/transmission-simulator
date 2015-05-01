import sys
import logging
import matplotlib.pyplot as plt
import numpy

from mpl_toolkits.mplot3d import Axes3D

from components.torque_converter import TorqueConverter

class TestEngine(object):
  def __init__(self):
    self.torque = 0
    self.speed = 0

  def GetEngineTorque(self):
    return self.torque
  def GetEngineSpeed(self):
    return self.speed

class TestTransmission(object):
  def __init__(self):
    self.torque = 0
    self.speed = 0

  def GetTransmissionTorque(self):
    return self.torque
  def GetTransmissionSpeed(self):
    return self.speed
  def StepOnce(self):
    pass

def main():
  logging.basicConfig(filename="torque_converter_test.log",
                      format="%(asctime)s %(module)s %(levelname)s %(message)s",
                      level=logging.INFO)

  logging.info("Test started.")

  engine = TestEngine()
  torque_converter = TorqueConverter()
  transmission = TestTransmission()

  torque_converter.Initialize("", engine, transmission)

  # speeds and torque values are for wide-open throttle
  engine_speeds  = [3000, 3000, 3000, 3000, 3000, 3000, 3000]
  engine_torques = [ 330,  330,  330,  330,  330,  330,  330]

  trans_speeds   = [   0,  500, 1000, 1500, 2000, 2500, 3000]
  trans_torques  = [ 800,  500,  300,  200,  150,  125,  100]

  for i in range(len(trans_speeds)):
    engine.speed = engine_speeds[i]
    engine.torque = engine_torques[i]

    transmission.speed = trans_speeds[i]
    transmission.torque = trans_torques[i]

    torque_converter.StepOnce()

if __name__ == "__main__":
  main()
