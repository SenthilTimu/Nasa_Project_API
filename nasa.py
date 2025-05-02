import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime
import mysql.connector as db

# Establish Mysql Connection
connection = db.connect(
    host = "localhost",
    user = "root",
    password = "root@123",
    db = "nasa"
)

# create a cursor object
cursor = connection.cursor()

st.set_page_config(layout="wide")
st.markdown("<h1 style='color:#1E90FF;'>🚀 NASA Asteroid Tracker 🌠</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True) #adding an horizontal line

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        "Asteroid Approaches",  # Menu title
        ["Filter Criteria", "Queries"],  # Menu options
        icons=["calendar", "calendar3"],  # Bootstrap icons
        menu_icon="cast",  # Icon for the menu title
        default_index=0
    )

if selected == "Filter Criteria":

    # Create 3 columns
    c1,a,c2,b,c3 = st.columns([0.2,0.1,0.2,0.1,0.2])

    with c1:
        # Magnitude
        min_mag = st.slider('Min Magnitude',min_value=13.8, max_value=32.61, value=(13.8, 32.61))  # default range (start, end)

        # Diameter
        min_diameter = st.slider('Min Estimated Diameter (km)',min_value = 0.00, max_value = 4.62, value = (0.00, 4.62))
        max_diameter = st.slider('Max Estimated Diameter (km)',min_value = 0.00, max_value = 10.33, value = (0.00, 10.33))

    with c2:
        # Velocity
        velocity = st.slider('Relative_velocity_kmph Range',min_value=1418.21,max_value=173071.83,value=(1418.21, 173071.83))

        # Astronomical
        astro = st.slider('Astronomical unit',min_value = 5.16453e-05,max_value = 0.4999515747,value = (5.16453e-05,0.4999515747))

        # Potentially Hazardous
        hazardous = st.selectbox('Only Show Potentially Hazardous', options=[0,1], index=0)

    with c3:
        # Date Range
        start_date = st.date_input("Start Date", datetime(2024, 1, 1))
        startingDate = start_date.strftime('%Y-%m-%d')
        end_date = st.date_input("End Date", datetime.today())
        endingDate = end_date.strftime('%Y-%m-%d')

    button = st.button('Filter')
    query = f"""
            SELECT
                asteroids.id as ID,
                asteroids.name Name,
                asteroids.absolute_magnitude_h "Absolute_Magnitude",
                asteroids.estimated_diameter_min_km Estimated_Minimum_Diameter,
                asteroids.estimated_diameter_max_km "Estimated_Maximum_Diameter",
                asteroids.is_potentially_hazardous_asteroid AS Potentially_Hazardous,
                close_approach.close_approach_date as CloseApproachDate,
                close_approach.relative_velocity_kmph Relative_Velocity_Kmph,
                close_approach.miss_distance_km "Miss_Distance_Km",
                close_approach.miss_distance_lunar as "Miss Distance Lunar",
                close_approach.orbiting_body Orbiting_Body
            FROM
                asteroids
            INNER JOIN close_approach ON asteroids.id = close_approach.neo_reference_id
            WHERE asteroids.absolute_magnitude_h BETWEEN %s AND %s
            AND asteroids.estimated_diameter_min_km BETWEEN %s AND %s
            AND asteroids.estimated_diameter_max_km BETWEEN %s AND %s
            AND close_approach.relative_velocity_kmph BETWEEN %s AND %s
            AND close_approach.astronomical_au BETWEEN %s AND %s
            AND asteroids.is_potentially_hazardous_asteroid  = %s
            AND close_approach.close_approach_date BETWEEN %s AND %s
            """
    
    params = [
        min_mag[0],min_mag[1],
        min_diameter[0],min_diameter[1],
        max_diameter[0],max_diameter[1],
        velocity[0],velocity[1],
        astro[0],astro[1],
        hazardous,
        startingDate,endingDate
    ]

    # -----Query Execution-----
    rows = []
    if button:
        cursor.execute(query,params)
        rows = cursor.fetchall()
    
    # -----Column names-----
    if cursor.description:
        columns = [desc[0] for desc in cursor.description]
    else:
        columns = []

    # -----Convert to DataFrame-----
    if rows and columns:
        df = pd.DataFrame(rows,columns=columns)
        # --- Show the result ---
        st.subheader("Filtered Asteroids")
        st.dataframe(df)

elif selected == "Queries":

    option = st.selectbox("Select your query", ['1.Count how many times each asteroid has approached Earth',
                                                '2.Average velocity of each asteroid over multiple approaches',
                                                '3.List top 10 fastest asteroids',
                                                '4.Find potentially hazardous asteroids that have approached Earth more than 3 times',
                                                '5.Find the month with the most asteroid approaches',
                                                '6.Get the asteroid with the fastest ever approach speed',
                                                '7.Sort asteroids by maximum estimated diameter (descending)',
                                                '8.Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)',
                                                '9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth',
                                                '10.List names of asteroids that approached Earth with velocity > 50,000 km/h',
                                                '11.Count how many approaches happened per month',
                                                '12.Find asteroid with the highest brightness (lowest magnitude value)',
                                                '13.Get number of hazardous vs non-hazardous asteroids',
                                                '14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance',
                                                '15.Find asteroids that came within 0.05 AU(astronomical distance)'])
    
    if option == '1.Count how many times each asteroid has approached Earth':
        cursor.execute("""SELECT
                            a.id,
                            a.name,
                            COUNT(ca.neo_reference_id) approach_count
                        FROM
                            asteroids a
                        INNER JOIN 
                            close_approach ca ON a.id = ca.neo_reference_id
                        GROUP BY
                            a.id, a.name
                        ORDER BY 
                            approach_count DESC
                       """)
        
    elif option == '2.Average velocity of each asteroid over multiple approaches':
        cursor.execute("""SELECT
                            a.id,
                            a.name,
                            avg(ca.relative_velocity_kmph) as avg_velocity_kmph
                        FROM
                            nasa.asteroids a
                        INNER JOIN
                            nasa.close_approach ca ON a.id=ca.neo_reference_id
                        GROUP BY
                            a.id, a.name
                        ORDER BY
                            avg_velocity_kmph DESC
                       """)
    
    elif option == '3.List top 10 fastest asteroids':
        cursor.execute("""SELECT 
                            a.name,
                            ca.relative_velocity_kmph
                        FROM 
                            nasa.close_approach ca
                        INNER JOIN 
                            nasa.asteroids a ON a.id = ca.neo_reference_id
                        ORDER BY
                            relative_velocity_kmph DESC
                        LIMIT 10
                        """)
        
    elif option == '4.Find potentially hazardous asteroids that have approached Earth more than 3 times':
        cursor.execute("""SELECT
                            a.id,
                            a.name,
                            count(*) as approach_count
                        FROM
                            nasa.asteroids a
                        INNER JOIN
                            nasa.close_approach ca ON a.id = ca.neo_reference_id
                        WHERE
                            a.is_potentially_hazardous_asteroid = TRUE
                        GROUP BY
                            a.id, a.name
                        HAVING approach_count > 3
                       """)
        
    elif option == '5.Find the month with the most asteroid approaches':
        cursor.execute("""
                        SELECT
                            MONTH(ca.close_approach_date) as approach_month,
                            count(*) as total_approaches
                        FROM
                            nasa.close_approach ca
                        GROUP BY
                            approach_month
                        ORDER BY
                            total_approaches DESC
                        LIMIT 1
                       """)
        
    elif option == '6.Get the asteroid with the fastest ever approach speed':
        cursor.execute("""SELECT
                            a.id,
                            a.name,
                            ca.relative_velocity_kmph
                        FROM
                            nasa.close_approach ca
                        INNER JOIN
                            nasa.asteroids a ON a.id = ca.neo_reference_id
                        ORDER BY
                            ca.relative_velocity_kmph DESC
                        LIMIT 1
                       """)
    
    elif option == '7.Sort asteroids by maximum estimated diameter (descending)':
        cursor.execute("""SELECT
                            a.id,
                            a.name,
                            ca.relative_velocity_kmph
                        FROM
                            nasa.close_approach ca
                        INNER JOIN
                            nasa.asteroids a ON a.id = ca.neo_reference_id
                        ORDER BY
                            ca.relative_velocity_kmph DESC
                        LIMIT 1
                       """)
        
    elif option == '8.Asteroids whose closest approach is getting nearer over time(Hint: Use ORDER BY close_approach_date and look at miss_distance)':
        cursor.execute("""WITH approach_data AS (
                            SELECT 
                                neo_reference_id,
                                close_approach_date,
                                miss_distance_km,
                                LEAD(miss_distance_km) OVER (PARTITION BY neo_reference_id ORDER BY close_approach_date) AS next_miss_distance
                            FROM 
                                nasa.close_approach
                        )

                        SELECT 
                            a.id,
                            a.name
                        FROM 
                            nasa.asteroids a
                        JOIN (
                            SELECT DISTINCT neo_reference_id
                            FROM approach_data
                            WHERE next_miss_distance IS NOT NULL
                            AND next_miss_distance < miss_distance_km
                        ) AS t
                        ON a.id = t.neo_reference_id;
                        """)
    
    elif option == '9.Display the name of each asteroid along with the date and miss distance of its closest approach to Earth':
        cursor.execute("""WITH closest_approach AS (
                            SELECT 
                                neo_reference_id,
                                close_approach_date,
                                miss_distance_km,
                                ROW_NUMBER() OVER (PARTITION BY neo_reference_id ORDER BY miss_distance_km ASC) AS rn
                            FROM 
                                nasa.close_approach
                        )

                        SELECT 
                            a.name,
                            ca.close_approach_date,
                            ca.miss_distance_km
                        FROM 
                            nasa.asteroids a
                        JOIN 
                            nasa.close_approach ca
                        ON 
                            a.id = ca.neo_reference_id
                        WHERE 
                            ca.rn = 1
                        ORDER BY 
                            ca.miss_distance_km ASC;
                       """)
    
    elif option == '10.List names of asteroids that approached Earth with velocity > 50,000 km/h':
        cursor.execute("""SELECT
                            DISTINCT a.name
                        FROM
                            nasa.asteroids a
                        INNER JOIN
                            nasa.close_approach ca ON a.id = ca.neo_reference_id
                        WHERE
                            ca.relative_velocity_kmph > 50000
                        """)
        
    elif option == '11.Count how many approaches happened per month':
        cursor.execute("""SELECT
                            DATE_FORMAT(close_approach_date, '%Y-%m') as close_approach_month,
                            count(*) as approach_count
                        FROM
                            nasa.close_approach
                        GROUP BY
                            close_approach_month
                        ORDER BY
                            close_approach_month
                        """)
    
    elif option == '12.Find asteroid with the highest brightness (lowest magnitude value)':
        cursor.execute("""SELECT 
                            name, 
                            absolute_magnitude_h
                        FROM 
                            nasa.asteroids
                        ORDER BY 
                            absolute_magnitude_h ASC
                        LIMIT 1
                        """)
        
    elif option == '13.Get number of hazardous vs non-hazardous asteroids':
        cursor.execute("""SELECT
                            is_potentially_hazardous_asteroid,
                            count(*) as count
                        FROM
                            nasa.asteroids
                        GROUP BY
                            is_potentially_hazardous_asteroid;
                        """)
        
    elif option == '14.Find asteroids that passed closer than the Moon (lesser than 1 LD), along with their close approach date and distance':
        cursor.execute("""SELECT
                            a.name,
                            ca.close_approach_date,
                            ca.miss_distance_lunar
                        FROM
                            nasa.asteroids a
                        INNER JOIN
                            nasa.close_approach ca ON a.id = ca.neo_reference_id
                        WHERE
                            ca.miss_distance_lunar < 1
                        ORDER BY
                            ca.miss_distance_lunar ASC
                        """)
    
    elif option == '15.Find asteroids that came within 0.05 AU(astronomical distance)':
        cursor.execute("""SELECT
                            a.name,
                            ca.close_approach_date,
                            ca.astronomical_au
                        FROM
                            nasa.asteroids a
                        INNER JOIN
                            nasa.close_approach ca ON a.id = ca.neo_reference_id
                        WHERE
                            ca.astronomical_au < 0.05
                        ORDER BY
                            ca.astronomical_au ASC
                       """)
        
    result = cursor.fetchall()
    st.dataframe(result)