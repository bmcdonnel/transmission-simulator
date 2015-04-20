import sys
import logging

from components.engine import Engine
from components.torque_converter import TorqueConverter
from components.transmission import Transmission
from components.vehicle_dynamics import VehicleDynamics

def main():
  logging.basicConfig(filename="simulation.log",
                      format="%(asctime)s %(module)s %(levelname)s %(message)s",
                      level=logging.INFO)

  logging.info("Simulation started.")

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

  logging.info("Running throttle schedule from " + sys.argv[1])

  while(True):
    engine.StepOnce(0)

if __name__ == "__main__":
  main()
