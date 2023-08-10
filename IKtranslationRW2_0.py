# -*- coding: utf-8 -*-
"""
Created on Mon Apr  3 11:38:29 2023

@author: ander
"""

import math


def recalculate(line, func_x, func_y, func_z):
    """
    Given a G-code line and three functions for X, Y, and Z,
    apply each function to its respective value in the line and
    return the modified line. If the line is not a valid G-code
    command, return it unchanged.
    """

    print("input line:", line)

    if not line.startswith("G") and not line.startswith("M"):
        return line  # Not a valid G-code command, so return it unchanged

    parts = line.split()
    x_val = y_val = z_val = a_val = b_val = 0  # Initialize all values to 0

    print("parts (before loop):", parts)

    x_indices = []
    y_indices = []
    z_indices = []

    for i in range(1, len(parts)):
        if parts[i].startswith("X"):
            x_val = float(parts[i][1:])
            x_indices.append(i)
        elif parts[i].startswith("Y"):
            y_val = float(parts[i][1:])
            y_indices.append(i)
        elif parts[i].startswith("Z"):
            z_val = float(parts[i][1:])
            z_indices.append(i)
        elif parts[i].startswith("A"):
            a_val = float(parts[i][1:])
        elif parts[i].startswith("B"):
            b_val = float(parts[i][1:])

    for i in x_indices:
        parts[i] = "X" + str(func_x(x_val, y_val, z_val, a_val, b_val))

    for i in y_indices:
        parts[i] = "Y" + str(func_y(x_val, y_val, z_val, a_val, b_val))
    
    for i in z_indices:
        parts[i] = "Z" + str(func_z(x_val, y_val, z_val, a_val, b_val))


    print("parts (after loop):", parts)
    print("output line:", line)


    return " ".join(parts)




def main(input_file, output_file, func_x, func_y, func_z):
    """
    Given an input G-code file, an output file name, and three functions
    for X, Y, and Z, read each line of the input file, apply the functions
    to the X, Y, and Z values, and write the modified line to the output file.
    """
    with open(input_file) as f:
        lines = f.readlines()

    with open(output_file, "w") as f:
        for line in lines:
            new_line = recalculate(line, func_x, func_y, func_z)
            f.write(new_line + "\n")


if __name__ == "__main__":
    

    
    """
    def func_x(x_val, y_val, z_val, a_val, b_val):
        return x_val * y_val

    def func_y(x_val, y_val, z_val, a_val, b_val):
        return y_val*2

    def func_z(x_val, y_val, z_val, a_val, b_val):
        return z_val*8
    """
    
    La = 28.4
    Lb = 47.7
    
    def func_x(x_val, y_val, z_val, a_val, b_val):
        return x_val + math.sin(math.radians(a_val)) * La + math.cos(math.radians(a_val)) * math.sin(math.radians(b_val)) * Lb

    def func_y(x_val, y_val, z_val, a_val, b_val):
        return y_val - La + math.cos(math.radians(a_val)) * La - math.sin(math.radians(a_val)) * math.sin(math.radians(b_val)) * Lb

    def func_z(x_val, y_val, z_val, a_val, b_val):
        return z_val + math.cos(math.radians(b_val)) * Lb - Lb

    input_file = "BENT2straightenedbunny2.gcode"
    output_file = "BENT2straightenedbunny2_IK.gcode"
    main(input_file, output_file, func_x, func_y, func_z)
