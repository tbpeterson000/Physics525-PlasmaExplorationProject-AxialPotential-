# Calculation of 1D Electrostatic Potential in a Magnetic Mirror 
## Overview
This project computes the axial electrostatic potential between the collisional Maxwellian source of a central cell and the bore of a magentic mirror fusion device. The goal of this work is to estimate the electrostatic environment seen by escaping ions for future research on direct energy conversion. Ion trajectories are calculated using the Lorentz force. The potential is reconstructed from binned ion density using the Boltzmann relation. The study is iterated to obtain a self-consistent, steady-state solution. 

## How To Run It
### Initial Study
1. Download and open axialpotential.mph file.
   - Ensure that the FittedPotential least-squares fit feature is disabled in the definitions node of "Component".
   - Ensure that the Electric Force feature in the charged particle tracing node is also disabled. 
2. In the form union node of the CoilGeometry select Build All.
3. In the Mesh feature select Build All.
4. Run the stationary and time-dependent study by selecting compute within the Study 1 node. 
5. Clear the density and volume tables in the results node after each run, and recompute them by evaluting the Density Volume Integration and Volume Integration features under derived values.
6. Create Excel files under the names density_integral.csv and slice_volume.csv 
7. Specify the filepaths to the Excel files created in step 6 under the density export and volume export features in the Export node. Export the data by selecting export.
8. Update the filepaths to density_integral.csv and slice_volume.csv in axialpotentialpost-processing.py
9. Run axialpotentialpost-processing.py
   
### Iterations
1. After completing the initial study outlined above,
   - Enable the FittedPotential least-squares fit feature in the definitions node of "Component".
   - Enable the the Electric Force feature in the charged particle tracing node.
2. In the Fitted Potential least-squares fit feature, update the filepath to phi_interpolation.csv, then select "Fit Parameters" and then "Plot"
3. Run the stationary and time-dependent study by selecting compute within the Study 1 node. 
4. Clear the density and volume tables after each run, and recompute them by evaluting the Density Volume Integration and Volume Integration features under derived values.
5. Export the data by selecting export in the density export and volume export features under the Export node.
6. Run axialpotentialpost-processing.py
7. Repeat steps 2-6 to continue iterating. 
8. Repeat until convergence.
