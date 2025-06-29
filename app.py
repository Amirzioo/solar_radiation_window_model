import streamlit as st
from calculations import calc_absorbed, calc_transmitted
from materials import materials
import matplotlib.pyplot as plt
import pandas as pd

# Initialize saved results if not exist
if "saved_results" not in st.session_state:
    st.session_state["saved_results"] = []

# Title and name input
st.title("Solar Radiation Simulation Tool")

case_name = st.text_input("Name of this case:", "My Simulation")

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

# Dimensions
width = st.sidebar.number_input("Window width [m]:", min_value=0.1, value=1.0)
height = st.sidebar.number_input("Window height [m]:", min_value=0.1, value=1.0)
area = width * height

# Irradiance
irradiance = st.sidebar.number_input("Solar irradiance [W/m2]:", min_value=0.0, value=800.0)

# Extra layer properties
st.sidebar.markdown("---")
st.sidebar.subheader("Extra Protective Layer")
extra_thickness_mm = st.sidebar.number_input("Extra layer thickness [mm]:", min_value=0.0, value=10.0)
extra_thickness_m = extra_thickness_mm / 1000.0
extra_absorption = st.sidebar.slider("Extra layer absorption coefficient [0-1]:", min_value=0.0, max_value=1.0, value=0.5)

# Show calculated area
st.sidebar.write(f"Calculated area: **{area:.2f} m²**")

# Base case (without extra layer)
rad_abs_base = calc_absorbed(tau, irradiance, area)
rad_trans_base = calc_transmitted(tau, irradiance, area)

# With extra layer
irradiance_after_extra = (1 - extra_absorption) * irradiance
rad_abs_extra = calc_absorbed(tau, irradiance_after_extra, area)
rad_trans_extra = calc_transmitted(tau, irradiance_after_extra, area)

# Compute reduction
reduction_percent = 100 * (1 - rad_trans_extra / rad_trans_base) if rad_trans_base > 0 else 0

# Display results
st.subheader("Results Without Extra Layer")
st.write(f"**Glazing:** {material_name}")
st.write(f"Absorbed radiation: **{rad_abs_base:.2f} W**")
st.write(f"Transmitted radiation: **{rad_trans_base:.2f} W**")

st.subheader("Results With Extra Layer")
st.write(f"Absorbed radiation: **{rad_abs_extra:.2f} W**")
st.write(f"Transmitted radiation: **{rad_trans_extra:.2f} W**")
st.write(f"Transmission reduction: **{reduction_percent:.1f}%**")

# Rectangle visualization
st.subheader("Window Dimensions")
fig, ax = plt.subplots(figsize=(4, 4))
rect = plt.Rectangle((0,0), width, height, color='lightblue')
ax.add_patch(rect)
ax.text(width/2, height/2, f"{width:.2f}m x {height:.2f}m",
        ha="center", va="center", fontsize=12, color="black")
ax.axis('off')
ax.set_xlim(-0.1, width + 0.1)
ax.set_ylim(-0.1, height + 0.1)
st.pyplot(fig)

# Save button
if st.button("💾 Save this case"):
    st.session_state["saved_results"].append({
        "Case": case_name,
        "Width [m]": width,
        "Height [m]": height,
        "Area [m2]": area,
        "Glazing": material_name,
        "Transmittance": tau,
        "Extra Thickness [mm]": extra_thickness_mm,
        "Extra Absorption": extra_absorption,
        "Irradiance [W/m2]": irradiance,
        "Absorbed Without Extra": rad_abs_base,
        "Transmitted Without Extra": rad_trans_base,
        "Absorbed With Extra": rad_abs_extra,
        "Transmitted With Extra": rad_trans_extra,
        "Reduction [%]": reduction_percent
    })

# Show saved cases
if st.session_state["saved_results"]:
    st.subheader("Saved Cases")

    # List of cases with delete buttons
    for idx, record in enumerate(st.session_state["saved_results"]):
        cols = st.columns((4,1))
        with cols[0]:
            st.write(f"**{record['Case']}** | Reduction: {record['Reduction [%]']:.1f}%")
        with cols[1]:
            if st.button("🗑️ Delete", key=f"del_{idx}"):
                st.session_state["saved_results"].pop(idx)
                st.experimental_rerun()

    # Dataframe table
    df = pd.DataFrame(st.session_state["saved_results"])
    st.dataframe(df)

    # Download button
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="saved_cases.csv",
        mime="text/csv"
    )
