import sys
import logging
import matplotlib.pyplot as plt
import numpy

from mpl_toolkits.mplot3d import Axes3D

from components.engine import Engine
from components.torque_converter import TorqueConverter
from components.transmission import Transmission
from components.vehicle_dynamics import VehicleDynamics

def main():
  logging.basicConfig(filename="simulation.log",
                      format="%(asctime)s %(module)s %(levelname)s %(message)s",
                      level=logging.INFO)

  logging.info("Simulation started.")

  throttle_steps = []

  engine = Engine()
  torque_converter = TorqueConverter()
  transmission = Transmission()
  vehicle_dynamics = VehicleDynamics()

  logging.info("Initializing vehicle components...")

  engine.Initialize("engine_model.csv", torque_converter)
  torque_converter.Initialize("torque_converter_model.csv", engine, transmission)
  transmission.Initialize("transmission_shift_schedule.csv", torque_converter, vehicle_dynamics)
  vehicle_dynamics.Initialize(transmission)

  engine.Start()

  for throttle in range(20, 50, 10):
    for j in range(100):
      engine.StepOnce(throttle)
      throttle_steps.append(throttle)

  PlotTorqueMap(engine.GetTorqueMap())
  PlotEngineInfo(engine.GetEngineSpeedSteps(),
                 engine.GetTorqueSteps(),
                 throttle_steps)
  plt.show()

def PlotTorqueMap(torque_map):
  figure = plt.figure(1)

  x = torque_map.keys()
  x.sort()
  y = torque_map.values()[0].keys()
  y.sort()

  Z = numpy.zeros((len(x), len(y)))

  for i in range(len(x)):
    for j in range(len(y)):
      # is this correct?
      Z[i][j] = torque_map[x[i]][y[j]]

  plot = figure.add_subplot(111, projection='3d')

  X, Y = numpy.meshgrid(x, y)
  plot.plot_surface(X, Y, Z, rstride=1, cstride=100)

def PlotEngineInfo(engine_speed_steps, torque_steps, throttle_steps):
  plt.figure(2)

  plt.subplot(131)
  plt.plot(range(len(engine_speed_steps)), engine_speed_steps, 'b-')

  plt.subplot(132)
  plt.plot(range(len(torque_steps)), torque_steps, 'r-')

  plt.subplot(133)
  plt.plot(range(len(throttle_steps)), throttle_steps, 'g-')

if __name__ == "__main__":
  main()
