import streamlit as st
import pandas as pd
import datetime

import pages.data.data_cache as cache


#page configs
st.set_page_config(page_title="Last Race", layout="wide")

#Side bar
st.sidebar.markdown("# Race Info")

st.sidebar.markdown("[Result](#race-results)", unsafe_allow_html=True)
st.sidebar.markdown("[Best Laps](#best-laps)", unsafe_allow_html=True)
st.sidebar.markdown("[Tyre Strategy](#tyre-strategy)", unsafe_allow_html=True)

# Input Race
race_name = st.text_input(label="Race Name", value="Monza")
year = st.number_input(label="Year", min_value=1950, max_value=datetime.datetime.now().year, value=2019)

if race_name is None or year is None:
    st.text("No Race Selected")
else:
        try:
            #Get Race Best Laps
            fastest_lap, best_laps, team_colors, session = cache.get_fastest_laps(race_name, year)
            st.markdown(f"<div style='text-align: center;'> <h1> {session} </h1> </div>", unsafe_allow_html=True)
        except Exception as e:
            print(e)
            st.text("Session not found")

        try:
            # Display Race Results
            result = cache.get_race_results(race_name, year).reset_index(drop=True)

            st.markdown(f"<div style='text-align: center;'> <h3> Race Results </h3> </div>", unsafe_allow_html=True)
            col1, col2, col3 = st.columns([1, 1, 1])

            with col1:
                try:
                    col1.image(image=cache.driver_profile_picture(result.iloc[1]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                
                col1.markdown("<h2 style='text-align: center;'> 🥈 " + result.iloc[1]['Name'] + "</h2>", unsafe_allow_html=True)
                
            with col2:
                try:
                    col2.image(image=cache.driver_profile_picture(result.iloc[0]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                    
                col2.markdown("<h2 style='text-align: center;'> 🥇 " + result.iloc[0]['Name'] + "</h2>", unsafe_allow_html=True)
                
            with col3:
                try:
                    col3.image(image=cache.driver_profile_picture(result.iloc[2]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                    
                col3.markdown("<h2 style='text-align: center;'> 🥉 " + result.iloc[2]['Name'] + "</h2>", unsafe_allow_html=True)

            result.index += 1
            st.table(result)
        except Exception as e:
            print(e)
            st.text("No Results Found")


        try:
            st.markdown(f"<div style='text-align: center;'> <h3> Best Laps </h3> </div>", unsafe_allow_html=True)

            fastLapCol, chartCol = st.columns([1, 2])

            #Display fastest Lap
            with fastLapCol:
                fastest_lap_time = datetime.datetime(1,1,1,0,0,0) + fastest_lap['LapTime']
                fastLapCol.markdown(f"<div style='text-align: center;'> <h2> Fastest Lap</h2> </div>", unsafe_allow_html=True)
                
                fastest_driver_name = result[result['Abbreviation'] == fastest_lap['Driver']]['Name'].values[0]
                
                try:
                    fastLapCol.image(image=cache.driver_profile_picture(fastest_driver_name, year))
                except Exception as e:
                    print(e)
                
                fastLapCol.markdown(f"<h4 style='text-align: center;'> {fastest_lap_time.strftime('%M:%S.%f')[:-3]} by {fastest_lap['Driver']} {fastest_lap['DriverNumber']} </h4>", unsafe_allow_html=True)
                
            #Display Best Laps
            with chartCol:
                fig = cache.get_best_laps_fig(best_laps, team_colors)
                chartCol.plotly_chart(fig, use_container_width=True)
                
                
            st.markdown(f"<div style='text-align: center;'> <h3> Tyre Strategy </h3> </div>", unsafe_allow_html=True)
        except Exception as e:
            print(e)
            st.text("No Best Laps Found")

        try:
            # Display Tyre Strategy
            st.pyplot(cache.get_tyre_strategy(race_name, year), use_container_width=True)
        except Exception as e:
            print(e)
            st.text("No Tyre Strategy Found")