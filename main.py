
from calculations import calc_absorbed, calc_transmited
from materials import materials

# Input from user #

window_area = input("Input window Area [m2]:")
solar_rad= input("Input solar irradiance [W/m2]:")


for key, data in materials.items():
    print(f"{key}){data['name']}")

material = int(input("Choose your material:"))

tau = materials[material]["transmittance"]

window_area = float(window_area)
solar_rad = float(solar_rad)



# Calculations #

rad_abs = calc_absorbed(tau, solar_rad, window_area)

rad_trans = calc_transmited(tau, solar_rad, window_area)


# Output #


print("\n=== Results ===")
print(f"Absorbed radiation: {rad_abs:.2f} W")
print(f"Transmitted radiation: {rad_trans:.2f} W")