import sys
from components.engine import Engine
from components.torque_converter import TorqueConverter
from components.transmission import Transmission
from components.vehicle_dynamics import VehicleDynamics

def main():
  engine = Engine()
  torque_converter = TorqueConverter()
  transmission = Transmission()
  vehicle_dynamics = VehicleDynamics()

  print "Initializing vehicle components..."

  engine.Initialize(sys.argv[1], torque_converter)
  torque_converter.Initialize(sys.argv[2], engine, transmission)
  transmission.Initialize(sys.argv[3], torque_converter, vehicle_dynamics)
  vehicle_dynamics.Initialize(transmission)

  print "Simulating throttle schedule from " + sys.argv[4]

  for i in range(10):
    print "throttle " + str(i) + "%, " + str(transmission.GetGear())
    engine.StepOnce(i)
    print str(vehicle_dynamics.GetFinalDriveSpeed()) + " RPM, " + str(vehicle_dynamics.GetVehicleSpeed()) + " MPH"

if __name__ == "__main__":
  main()
