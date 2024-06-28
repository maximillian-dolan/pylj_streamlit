from pylj import mc, md, sample
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.subplots as sp

options = st.popover('options')

with options:
    number_of_particles = st.slider('Number of particles', min_value = 1, max_value = 50, step = 1, value = 20)
    box_length = st.slider('Box Length', min_value = 5, max_value = 20, step = 1, value = 100)
    number_of_steps = st.slider('Number of steps', min_value = 100, max_value = 5000, step = 100, value = 5000)
    temperature = st.slider('Temperature', min_value = 0, max_value = 1500, step = 100, value = 1000)

def md_simulation(number_of_particles, temperature, box_length, number_of_steps, sample_frequency):
    # Initialise the system
    system = md.initialise(number_of_particles, temperature, box_length, 'square')
    # This sets the sampling class
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
            current_positions['velocity'] = np.sqrt(system.particles['xvelocity']**2 + system.particles['yvelocity']**2)
            current_positions['energy'] = system.particles['energy']
            df = pd.DataFrame(current_positions)
            positions = pd.concat([positions, df], ignore_index=True)

    return system, positions

if st.button('generate'):
    system, positions = md_simulation(number_of_particles, temperature, box_length, number_of_steps, 100)
else:
    system, positions = md_simulation(number_of_particles, temperature, box_length, 100, 100)


#=================================================
#=================================================
#Creating animation
#=================================================
animation = px.scatter(positions,
                 x = 'xposition',
                 y = 'yposition',
                 animation_frame = 'cycle',
                 #animation_group = 'particle',
                 range_x = [0, box_length*1e-10],
                 range_y = [0, box_length*1e-10]
                 )

# Update animation axes to just be a box
animation.update_yaxes(showgrid=False,
                       #showline = True,
                       #linewidth = 1,
                       #mirror = True,
                       zeroline = False,
                       showticklabels=False,
                       title_text = '')
animation.update_xaxes(showgrid=False,
                       #showline = True,
                       #linewidth = 1,
                       #mirror = True,
                       zeroline = False,
                       showticklabels=False,
                       title_text = '')
#=================================================
#=================================================
velocity_fig = px.bar(positions,
                    x = 'particle',
                    y = 'velocity',
                    animation_frame = 'cycle',
                    animation_group = 'particle',
                    range_y = [0, max(positions['velocity'])]
                    )

energy_fig = px.bar(positions,
                    x = 'particle',
                    y = 'energy',
                    animation_frame = 'cycle',
                    animation_group = 'particle',
                    range_y = [min(positions['energy']), max(positions['energy'])]
                    )

col1,col2 = st.columns(2)


with col1:
    st.plotly_chart(animation, use_container_width = True)

with col2:
    st.plotly_chart(velocity_fig, use_container_width = True)
