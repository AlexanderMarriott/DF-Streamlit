import random
import requests
import streamlit as st
import pandas as pd

st.title('Pokeview Center!')
st.header('Welcome to the Pokeview Center! Here you can learn about random Pokémon!')
st.divider()

col1, col2, col3 = st.columns([1.5,2,1])
with col2:
    explore_random_pokemon = st.button("Explore 3 Random Pokémon")

if explore_random_pokemon:
    pokemon_data = []  # List to store dictionaries of Pokémon data

    for _ in range(3):  # Fetch data for 3 random Pokémon
        random_identifier = random.randint(1, 151)
        pokemon_url = f"https://pokeapi.co/api/v2/pokemon/{random_identifier}"
        response = requests.get(pokemon_url).json()

        # Create a dictionary for the current Pokémon
        pokemon = {
            'name': response['name'].title(),
            'height': response['height'],
            'weight': response['weight'],
            'base_experience': response['base_experience'],
            'image': response['sprites']['other']['official-artwork']['front_default'],
            'cry': response.get('cries', {}).get('latest', ''),  
            'attacks': [item['move']['name'] for item in response['moves'][:5]],
        }
        pokemon_data.append(pokemon)  # Add the dictionary to the list

    for pokemon in pokemon_data:
        info, picture = st.columns([1, 1])
        with info:
            st.write(f"Name: {pokemon['name']}")
            st.write(f"Height: {pokemon['height']} Pokemeters")
            st.write(f"Weight: {pokemon['weight']} Pokegrams")
            st.write(f"Base Experience: {pokemon['base_experience']}")
            st.write("Attacks:")
            for attack in pokemon['attacks']:
                st.markdown(f"- {attack}")
        
        with picture:
            st.image(pokemon['image'], caption=f"{pokemon['name']}", use_column_width=True)
            if pokemon['cry']:  # Check if 'cry' key exists and has a value
                st.audio(pokemon['cry'], format='audio/mp3', start_time=0)
        
        
        st.markdown("---")

        stats_data = {
            'Name': [pokemon['name'] for pokemon in pokemon_data],
            'Height': [pokemon['height'] for pokemon in pokemon_data]
        }

    df_stats = pd.DataFrame(stats_data)

    st.header("Pokémon height Comparison")
    st.bar_chart(df_stats.set_index('Name'))

st.divider()