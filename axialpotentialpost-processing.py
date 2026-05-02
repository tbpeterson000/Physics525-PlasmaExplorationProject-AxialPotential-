import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



density_file = r"C:/Users/tbpet/WHAM/Simulations/density_integral.csv"
volume_file  = r"C:/Users/tbpet/WHAM/Simulations/slice_volume.csv"

interp_file = "phi_interpolation.csv"
history_file = "axial_potential_history.csv"

alpha = 0.25  # new solution weight

# read one-row COMSOL/Excel-style files
density_integral = pd.read_csv(density_file, header=None).to_numpy().flatten().astype(float)
slice_volume = pd.read_csv(volume_file, header=None).to_numpy().flatten().astype(float)

# First value is COMSOL time label
density_integral = density_integral[1:]
slice_volume = slice_volume[1:]

# average density in each z-bin
n_avg = density_integral / slice_volume

# z-bin setup
z_start = 0.58
dz = 0.02
z_center = z_start + dz*(np.arange(len(n_avg)) + 0.5)

# Boltzmann relation: new raw potential
Te_eV = 100.0
n_ref = n_avg[0]
phi_new = Te_eV * np.log(n_avg / n_ref)

# Load previous applied solution, if it exists
if os.path.exists(interp_file):
    old_interp = pd.read_csv(interp_file, header=None)
    phi_old = old_interp.iloc[:, 1].to_numpy().astype(float)

    if len(phi_old) != len(phi_new):
        raise ValueError("Old interpolation file has different number of points than new solution.")

    phi_V = (1 - alpha) * phi_old + alpha * phi_new
else:
    # First run: no previous solution, so use 100% of the new potential from zero
    phi_old = np.zeros_like(phi_new)
    phi_V = phi_new

# save full data
out = pd.DataFrame({
    "z_center": z_center,
    "density_integral": density_integral,
    "slice_volume": slice_volume,
    "n_avg": n_avg,
    "phi_new_raw_V": phi_new,
    "phi_old_V": phi_old,
    "phi_applied_V": phi_V
})

out.to_csv("processed_density_potential.csv", index=False)

# save COMSOL interpolation file: z, relaxed phi
out[["z_center", "phi_applied_V"]].to_csv(
    interp_file,
    index=False,
    header=False
)

# plot both raw and relaxed potential
plt.figure()
plt.plot(z_center, phi_new, marker="o", color = "blue", linewidth = 4,label="New Phi Curve")
plt.plot(z_center, phi_V, marker="o", color = "red", linewidth = 3, linestyle="--",label="Relaxed Phi Curve")
plt.xlabel("z [m]")
plt.ylabel("phi [V]")
plt.title("Axial Potential with 25% Relaxation")
plt.grid(True)
plt.legend()
plt.show()

run_number = 1
if os.path.exists(history_file):
    old = pd.read_csv(history_file)
    if "run" in old.columns:
        run_number = old["run"].max() + 1

# append raw and relaxed solution to history
run_data = pd.DataFrame({
    "z_center": z_center,
    "phi_raw_V": phi_new,
    "phi_relaxed_V": phi_V,
    "phi_old_V": phi_old
})

run_data["run"] = run_number
run_data["alpha"] = alpha

run_data.to_csv(
    history_file,
    mode="a",
    header=not os.path.exists(history_file),
    index=False
)

print("Saved relaxed potential to phi_interpolation.csv")
print("Saved run to axial_potential_history.csv")


