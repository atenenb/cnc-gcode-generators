#!/usr/bin/env python

step_down = 0.2
start_z = 0
end_z = -4
start_x = 37.0
end_x = 27.0
retract = 0.5
feed_rate = 30

work_z_level = start_z
g_code = "%\n"
g_code += "G0 X%.4f Z%4f\n" % (start_x, start_z)


while work_z_level > end_z:
    work_z_level -= step_down
    g_code += "G1 Z%.4f F%4f\n" % (work_z_level, feed_rate)
    g_code += "G1 X%.4f F%4f\n" % (end_x, feed_rate)
    g_code += "G0 Z%.4f \n" % (start_z + retract)
    g_code += "G0 X%.4f \n" % start_x

g_code += "\n"
g_code += "%\n"

print(g_code)

