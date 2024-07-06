from pylj import mc, md, sample
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def mc_simulation(number_of_particles, temperature, box_length, number_of_steps, sample_frequency):
    # Initialise the system placing the particles on a square lattice
    system = mc.initialise(number_of_particles, temperature, box_length, 'square')
    # This initialises the dataframe
    positions = pd.DataFrame({})
    current_positions = {}
    # Compute the energy of the system
    system.compute_energy()
    system.old_energy = system.energies.sum()
    # Add this energy to the energy sample array
    system.mc_sample()
    # Begin the monte carlo loop
    for i in range(0, number_of_steps):
        system.step += 1
        # Select a random particle to remove
        system.select_random_particle()
        # Select a random position to replace that particle
        system.new_random_position()
        # Compute the new energy of the system
        system.compute_energy()
        system.new_energy = system.energies.sum()
        # Assess the Metropolis condition
        if mc.metropolis(temperature, system.old_energy, system.new_energy):
            system.accept()
        else:
            system.reject()
        # Add this energy to the energy sample array
        system.mc_sample()
        # At a given frequency sample the positions and plot
        if i % sample_frequency == 0:
            current_positions['cycle'] = [i]*number_of_particles
            current_positions['xposition'] = system.particles['xposition']
            current_positions['yposition'] = system.particles['yposition']
            current_positions['particle'] = np.arange(number_of_particles)
            current_positions['velocity'] = np.sqrt(system.particles['xvelocity']**2 + system.particles['yvelocity']**2)
            current_positions['energy'] = system.particles['energy']
            df = pd.DataFrame(current_positions)
            positions = pd.concat([positions, df], ignore_index=True)
    return system, positions

def main():
    options = st.popover('options')

    with options:
        number_of_particles = st.slider('Number of particles', min_value = 1, max_value = 50, step = 1, value = 20)
        box_length = st.slider('Box Length', min_value = 5, max_value = 20, step = 1, value = 100)
        number_of_steps = st.slider('Number of steps', min_value = 10, max_value = 500, step = 10, value = 250)
        temperature = st.slider('Temperature', min_value = 0, max_value = 1500, step = 100, value = 1000)

    if st.button('generate'):
        system, positions = mc_simulation(number_of_particles, temperature, box_length, number_of_steps, 10)
    else:
        system, positions = mc_simulation(number_of_particles, temperature, box_length, 100, 10)

    #=================================================
    #=================================================
    #Creating animation
    #=================================================
    animation = px.scatter(positions,
                    x = 'xposition',
                    y = 'yposition',
                    animation_frame = 'cycle',
                    animation_group = 'particle',
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
        st.plotly_chart(energy_fig, use_container_width = True)

if __name__ == "__main__":
    main()