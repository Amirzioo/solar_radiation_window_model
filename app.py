import streamlit as st
from calculations import calc_absorbed, calc_transmitted
from materials import materials

# Sidebar Inputs
st.sidebar.title("Input Parameters")

# Material selection dropdown
material_options = {data["name"]: data["transmittance"] for data in materials.values()}
material_name = st.sidebar.selectbox(
    "Select glazing type:",
    list(material_options.keys())
)

# Get transmittance
tau = material_options[material_name]

# Input fields
area = st.sidebar.number_input("Window area [m2]:", min_value=0.0, value=1.0)
irradiance = st.sidebar.number_input("Solar irradiance [W/m2]:", min_value=0.0, value=800.0)

# Button
if st.sidebar.button("Calculate"):
    # Calculations
    rad_abs = calc_absorbed(tau, irradiance, area)
    rad_trans = calc_transmitted(tau, irradiance, area)

    # Results
    st.subheader("Results")
    st.write(f"**Selected material:** {material_name}")
    st.write(f"Absorbed radiation: **{rad_abs:.2f} W**")
    st.write(f"Transmitted radiation: **{rad_trans:.2f} W**")

    # Bar chart
    st.subheader("Radiation Distribution")
    st.bar_chart({"Radiation (W)": [rad_abs, rad_trans]}, 
                 use_container_width=True)