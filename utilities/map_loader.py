import logging

class MapLoader(object):
  def __init__(self, filename):
    self._filename = filename

  def LinearlyInterpolate(self):
    value_count = 0
    xyz_map = dict()

    with open(self._filename) as f:
      # drop the first item of the first line since its just a
      # spacer representing the throttle position column
      x_values = f.readline().split()[1:]

      logging.info(str(len(x_values)) + " X values")

      # count the rest of the lines remaining in the file (excluding the first line of RPM values)
      y_value_count = sum(1 for line in f)

      logging.info(str(y_value_count) + " Y values")

      # seek back to the second line to start loading torque values
      f.seek(0)
      f.readline()

      for line in f:
        # split off the first value representing the throttle position
        y = int(line.split(' ', 1)[0])

        if y not in xyz_map:
          xyz_map[y] = dict()

        # the rest are torque values for each RPM at that throttle position
        z_values = line.split()[1:]

        if len(z_values) != len(x_values):
          raise Exception('Each X value must have a Z value for Y value ' + str(y))

        for i in range(len(x_values) - 1):
          # grab two x values
          x_i = int(x_values[i])
          x_j = int(x_values[i + 1])
          x_diff = x_j - x_i

          # grab the two associated z values
          z_i = int(z_values[i])
          z_j = int(z_values[i + 1])
          z_diff = z_j - z_i

          # force floating point division
          ratio = z_diff / float(x_diff)

          for j in range(x_diff + 1):
            x = x_i + j
            z = int(z_i + (ratio * j))

            if z < 0:
              raise Exception('negative Z {} for X {} resulting from X({}, {}), Z({}, {}), ratio {} at Y {}'.format(z, x, x_i, x_j, z_i, z_j, ratio, y))

            xyz_map[y][x] = z
            value_count += 1

    return xyz_map, value_count

