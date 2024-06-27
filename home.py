from pylj import mc, md, sample
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def md_simulation(number_of_particles, temperature, box_length, number_of_steps, sample_frequency):
    # Initialise the system
    system = md.initialise(number_of_particles, temperature, box_length, 'square')
    # This sets the sampling class

    xpositions = []
    ypositions = []
    positions = pd.DataFrame({})
    current_positions = {}

    #sample_system = sample.MaxBolt(system)# Start at time 0
    system.time = 0
    # Begin the molecular dynamics loop
    for i in range(0, number_of_steps):
        # Run the equations of motion integrator algorithm, this 
        # includes the force calculation
        system.integrate(md.velocity_verlet)
        # Sample the thermodynamic and structural parameters of the system
        system.md_sample()
        # Allow the system to interact with a heat bath
        system.heat_bath(temperature)
        # Iterate the time
        system.time += system.timestep_length
        system.step += 1

        # At a given frequency sample the positions and plot the RDF
        if i % sample_frequency == 0 or i == 0: 
            current_positions['cycle'] = [i]*number_of_particles
            current_positions['xposition'] = system.particles['xposition']
            current_positions['yposition'] = system.particles['yposition']
            current_positions['particle'] = np.arange(number_of_particles)
            xpositions.append(system.particles['xposition'])
            df = pd.DataFrame(current_positions)
            positions = pd.concat([positions, df], ignore_index=True)

    return system, positions, xpositions

system, positions, xpositions = md_simulation(20, 1000, 100, 5000, 100)

fig = px.scatter(positions,
                 x = 'xposition',
                 y = 'yposition',
                 animation_frame = 'cycle',
                 animation_group = 'particle'
                 )

st.plotly_chart(fig)
