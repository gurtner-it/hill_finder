


import subprocess

process1 = subprocess.Popen(["python3", "01_plot_track.py"]) # Create and launch process pop.py using python interpreter
process2 = subprocess.Popen(["python3", "02_plot_elevation.py"])
process3 = subprocess.Popen(["python3", "03_plot_gradient.py"])
process4 = subprocess.Popen(["python3", "04_gradient_analysis.py"])


process1.wait(100) # Wait for process1 to finish (basically wait for script to finish)
process2.wait(100)
process3.wait(100)
process4.wait(100)