#Get information about a specific race

import streamlit as st
import datetime

import pages.data.Cache as Cache


#Page Configs
st.set_page_config(page_title="Last Race", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

#Side Bar Settings
st.sidebar.markdown("# Race Info")

st.sidebar.markdown("[Result](#race-results)", unsafe_allow_html=True)
st.sidebar.markdown("[Best Laps](#best-laps)", unsafe_allow_html=True)
st.sidebar.markdown("[Tyre Strategy](#tyre-strategy)", unsafe_allow_html=True)


#Input Race Name and Year
race_name = st.text_input(label="Race Name", value="Monza")
year = st.number_input(label="Year", min_value=1950, max_value=datetime.datetime.now().year, value=2019)

race = Cache.get_Race(race_name, year)

#Page Content
if race is None:
    st.text("No Race Found")
else:
        try: #Some times the session is not available
            st.markdown(f"<div style='text-align: center;'> <h1> {race.session} </h1> </div>", unsafe_allow_html=True)
        except Exception as e:
            print(e)
            st.markdown(f"<div style='text-align: center;'> <h1> {race_name} {year} </h1> </div>", unsafe_allow_html=True)

        try:
            # Display Race Results
            st.markdown(f"<div style='text-align: center;'> <h3> Race Results </h3> </div>", unsafe_allow_html=True)
            SecondPlaceCol, FirstPlaceCol, ThirdPlaceCol = st.columns([1, 1, 1])

            with SecondPlaceCol:
                try:
                    SecondPlaceCol.image(image=Cache.driver_profile_picture(race.results.iloc[1]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                            
                if 'Name' in race.results.iloc[1]:
                    SecondPlaceCol.markdown("<h2 style='text-align: center;'> 🥈 " + race.results.iloc[1]['Name'] + "</h2>", unsafe_allow_html=True)
                
            with FirstPlaceCol:
                try:
                    FirstPlaceCol.image(image=Cache.driver_profile_picture(race.results.iloc[0]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                    
                if 'Name' in race.results.iloc[0]:    
                    FirstPlaceCol.markdown("<h2 style='text-align: center;'> 🥇 " + race.results.iloc[0]['Name'] + "</h2>", unsafe_allow_html=True)
                
            with ThirdPlaceCol:
                try:
                    ThirdPlaceCol.image(image=Cache.driver_profile_picture(race.results.iloc[2]['Name'], year), width=100, use_column_width=True)
                except Exception as e:
                    print(e)
                    
                if 'Name' in race.results.iloc[2]:
                    ThirdPlaceCol.markdown("<h2 style='text-align: center;'> 🥉 " + race.results.iloc[2]['Name'] + "</h2>", unsafe_allow_html=True)

            #Display full race results
            st.table(race.results)
        except Exception as e:
            print(e)
            st.text("Race Results Not Available")


        try:
            st.markdown(f"<div style='text-align: center;'> <h3> Best Laps </h3> </div>", unsafe_allow_html=True)

            fastLapCol, chartCol = st.columns([1, 1])

            #Display fastest Lap
            with fastLapCol:
                fastest_lap_time = datetime.datetime(1,1,1,0,0,0) + race.fastest_lap['LapTime']
                fastLapCol.markdown(f"<div style='text-align: center;'> <h2> Fastest Lap</h2> </div>", unsafe_allow_html=True)
                
                try:
                    fastLapCol.pyplot(race.heatmap, use_container_width=True)
                except Exception as e:
                    print(e)
                    
                    try:
                        fastest_driver_name = race.results[race.results['Abbreviation'] == race.fastest_lap['Driver']]['Name'].values[0]
                        fastLapCol.image(image=Cache.driver_profile_picture(fastest_driver_name))
                    except Exception as e:
                        print(e)
                
                fastLapCol.markdown(f"<h4 style='text-align: center;'> {fastest_lap_time.strftime('%M:%S.%f')[:-3]} by {race.fastest_lap['Driver']} {race.fastest_lap['DriverNumber']} </h4>", unsafe_allow_html=True)
                
            #Display Best Laps
            with chartCol:
                chartCol.plotly_chart(race.fig, use_container_width=True)
                
                
            st.markdown(f"<div style='text-align: center;'> <h3> Tyre Strategy </h3> </div>", unsafe_allow_html=True)
        except Exception as e:
            print(e)
            st.text("Best Laps Not Available")

        try:
            # Display Tyre Strategy
            st.pyplot(race.tyre_strategy, use_container_width=True)
        except Exception as e:
            print(e)
            st.text("Tyre Strategy Not Available")