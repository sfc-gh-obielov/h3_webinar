import streamlit as st
import pandas as pd
import pydeck as pdk
import branca.colormap as cm
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col
from typing import List
import json
from PIL import Image
image = Image.open('./favicon.png')
st.set_page_config(page_title="H3: Simplifying the World's Map", page_icon=image)
st.header("What is H3", divider="rainbow")

session = Session.builder.configs(st.secrets["geodemo"]).create()
# st.set_page_config(page_title="H3 in Streamlit", layout="wide")

st.markdown("H3 Discrete Global Grid (Spatial Index) is a way to divide the world into a grid of hexagonal cells of equal sizes, "
            "each with a unique identifier (string or integer).") 
    
col1, col2, col3 = st.columns(3)
with col2:
    st.write("**String**")
    st.text('8c274daeb7a0bff')
    st.text('8c2ab2d9294c5ff')
    st.text('8c2ab2da36605ff')

with col3:
    st.write("**Integer**")
    st.text('631195381387627519')
    st.text('631255110006392319')
    st.text('631255110288541183')

with col1:
    st.image('https://viennadatasciencegroup.at/post/2019-11-21-h3spark/featured.png',  width=160)

st.write("- Hierarchical structure with 16 different resolutions.")
st.write("- Each point or area on the Earth's surface can be encoded.")
st.write("- Enables the use of simpler and more efficient geospatial algorithms and visualizations.")

# ------ Visualisation 1 ---------
@st.cache_resource(ttl="4d")
def get_h3point_df(resolution: float, row_count: int) -> pd.DataFrame:
    return session.sql(
        f"select distinct h3_point_to_cell_string(ST_POINT(UNIFORM( -180 , 180 , random()), UNIFORM( -90 , 90 , random())), {resolution}) as h3 from table(generator(rowCount => {row_count}))"
    ).to_pandas()


@st.cache_resource(ttl="4d")
def get_coverage_layer(df: pd.DataFrame, line_color: List) -> pdk.Layer:
    return pdk.Layer(
        "H3HexagonLayer",
        df,
        get_hexagon="H3",
        stroked=True,
        filled=False,
        auto_highlight=True,
        elevation_scale=45,
        pickable=True,
        extruded=False,
        get_line_color=line_color,
        line_width_min_pixels=1,
    )

min_v_1, max_v_1, v_1, z_1, lon_1, lat_1 = ( 0, 2, 0, 1, 0.9982847947205775, 2.9819747220001886,)
col1, col2 = st.columns([70, 30])
with col1:
    h3_resolut_1 = st.slider(
        "H3 resolution", min_value=min_v_1, max_value=max_v_1, value=v_1)

with col2:
    levels_option = st.selectbox("Levels", ("One", "Two", "Three"), 1)

df = get_h3point_df(h3_resolut_1, 100000)
layer_coverage_1 = get_coverage_layer(df, [36, 191, 242])

visible_layers_coverage_1 = [layer_coverage_1]

if levels_option == "Two":
    df_coverage_level_1 = get_h3point_df(h3_resolut_1 + 1, 100000)
    layer_coverage_1_level_1 = get_coverage_layer(df_coverage_level_1, [217, 102, 255])
    visible_layers_coverage_1 = [layer_coverage_1, layer_coverage_1_level_1]

if levels_option == "Three":
    df_coverage_level_1 = get_h3point_df(h3_resolut_1 + 1, 100000)
    layer_coverage_1_level_1 = get_coverage_layer(df_coverage_level_1, [217, 102, 255])

    df_coverage_level_2 = get_h3point_df(h3_resolut_1+2, 1000000)

    layer_coverage_1_level2 = get_coverage_layer(df_coverage_level_2, [18, 100, 129])
    visible_layers_coverage_1 = [
        layer_coverage_1,
        layer_coverage_1_level_1,
        layer_coverage_1_level2, ]

st.pydeck_chart(
    pdk.Deck(map_provider='carto', 
        map_style='light',
        initial_view_state=pdk.ViewState(
            latitude=lat_1, longitude=lon_1, zoom=z_1, height=400
        ),
        tooltip={"html": "<b>ID:</b> {H3}", "style": {"color": "white"}},
        layers=visible_layers_coverage_1,
    )
)

st.write("**Key Benefits:**")
st.write("**Efficiency.** Analytics are faster and more computationally efficient.")
st.write("**Flexibility.** Allows for the combination of datasets into one layer for ease of comparison and analysis.")
st.write("**Objectivity.** Removes bias associated with traditional administrative geographies.")
st.write("**Impact.** Results in visuals that are more impactful and much easier to understand.")

# ------ Visualisation 1 End ---------
st.divider()
st.subheader("H3 in Snowflake")
col1, col2, col3 = st.columns(3)
with col1:
    st.text('H3_LATLNG_TO_CELL')
    st.text('H3_POINT_TO_CELL')
    st.text('H3_CELL_TO_POINT')
    st.text('H3_CELL_TO_CHILDREN')
    st.text('H3_CELL_TO_PARENT')
with col2:
    st.text('H3_COVERAGE')
    st.text('H3_POLYGON_TO_CELLS')
    st.text('H3_GRID_DISTANCE')
    st.text('H3_GRID_DISK')
    st.text('H3_GRID_PATH')
with col3:
    st.text('H3_CELL_TO_BOUNDARY')
    st.text('H3_GET_RESOLUTION')
    st.text('H3_INT_TO_STRING')
    st.text('H3_STRING_TO_INT')

# ------ Visualisation 2 ---------
col1, col2, col3 = st.columns(3)

with col1:
    poly_scale_2 = st.selectbox("Scale of polygon", ("Global", "Local"), index=1)
    if poly_scale_2 == 'Global':
        min_v_2, max_v_2, v_2, z_2, lon_2, lat_2 = 2, 5, 4, 2, -94.50284957885742, 38.51405689475766
    else:
        min_v_2, max_v_2, v_2, z_2, lon_2, lat_2 = 7, 10, 9, 9, -73.98452997207642, 40.74258515841464

with col2:
    original_shape_2 = st.selectbox("Show original shape", ("Yes", "No"),  index=0)

with col3:
    h3_res_2 = st.slider( "H3 resolution ", min_value=min_v_2, max_value=max_v_2, value=v_2)

@st.cache_resource(ttl="4d")
def get_df_shape_2(poly_scale_2: str) -> pd.DataFrame:
    df = session.sql(
        f"select geog from snowpublic.streamlit.h3_polygon_spherical where scale_of_polygon = '{poly_scale_2}'"
    ).to_pandas()
    df["coordinates"] = df["GEOG"].apply(lambda row: json.loads(row)["coordinates"][0])
    return df


@st.cache_resource(ttl="4d")
def get_layer_shape_2(df: pd.DataFrame, line_color: List) -> pdk.Layer:
    return pdk.Layer("PolygonLayer", 
                     df, 
                     opacity=0.9, 
                     stroked=True, 
                     get_polygon="coordinates",
                     filled=False,
                     extruded=False,
                     wireframe=True,
                     get_line_color=line_color,
                     line_width_min_pixels=1)

@st.cache_resource(ttl="4d")
def get_df_coverage_2(h3_res_2: float, poly_scale_2: str) -> pd.DataFrame:
    return session.sql(
        f"select value::string as h3 from snowpublic.streamlit.h3_polygon_planar, TABLE(FLATTEN(h3_coverage_strings(geog, {h3_res_2}))) where scale_of_polygon = '{poly_scale_2}'"
    ).to_pandas()

@st.cache_resource(ttl="4d")
def get_layer_coverage_2(df_coverage_2: pd.DataFrame, line_color: List) -> pdk.Layer:
    return pdk.Layer("H3HexagonLayer", 
                     df_coverage_2, 
                     get_hexagon="H3", 
                     extruded=False,
                     stroked=True, 
                     filled=False, 
                     get_line_color=line_color, 
                     line_width_min_pixels=1)

@st.cache_resource(ttl="4d")
def get_df_polyfill_2(h3_res_2: float, poly_scale_2: str) -> pd.DataFrame:
    return session.sql(
        f"select value::string as h3 from snowpublic.streamlit.h3_polygon_planar, TABLE(FLATTEN(h3_polygon_to_cells_strings(geog, {h3_res_2}))) where scale_of_polygon = '{poly_scale_2}'"
    ).to_pandas()

@st.cache_resource(ttl="4d")
def get_layer_polyfill_2(df_polyfill_2: pd.DataFrame, line_color: List) -> pdk.Layer:
    return pdk.Layer("H3HexagonLayer", 
                     df_polyfill_2, 
                     get_hexagon="H3", 
                     extruded=False,
                     stroked=True, 
                     filled=False, 
                     get_line_color=line_color, 
                     line_width_min_pixels=1)

df_shape_2 = get_df_shape_2(poly_scale_2)
layer_shape_2 = get_layer_shape_2(df_shape_2, [217, 102, 255])

df_coverage_2 = get_df_coverage_2(h3_res_2, poly_scale_2)
layer_coverage_2 = get_layer_coverage_2(df_coverage_2, [18, 100, 129])

df_polyfill_2 = get_df_polyfill_2(h3_res_2, poly_scale_2)
layer_polyfill_2 = get_layer_polyfill_2(df_polyfill_2, [36, 191, 242])

if original_shape_2 == "Yes":
    visible_layers_coverage_2 = [layer_coverage_2, layer_shape_2]
    visible_layers_polyfill_2 = [layer_polyfill_2, layer_shape_2]
else:
    visible_layers_coverage_2 = [layer_coverage_2]
    visible_layers_polyfill_2 = [layer_polyfill_2]

col1, col2 = st.columns(2)

with col1:
    st.pydeck_chart(pdk.Deck(map_provider='carto', map_style='light',
                             initial_view_state=pdk.ViewState(
                                 latitude=lat_2,
                                 longitude=lon_2, 
                                 zoom=z_2, 
                                 width = 350, 
                                 height = 250),
                             layers=visible_layers_coverage_2))
    st.caption('H3_COVERAGE')

with col2:
    st.pydeck_chart(pdk.Deck(map_provider='carto', map_style='light',
                             initial_view_state=pdk.ViewState(
                                 latitude=lat_2,
                                 longitude=lon_2,
                                 zoom=z_2, 
                                 width = 350, 
                                 height = 250),
                             layers=visible_layers_polyfill_2))
    st.caption('H3_POLYGON_TO_CELLS')

# ------ Visualisation 2 End ---------
st.divider()

st.header("How are organizations using Spatial Indexes?")

st.markdown("""**Delivery & quick commerce.** To evaluate business critical performance indicators such as delivery delays and errors.\n
**Logistics & fleet management.** To optimize routings, delivery times and better manage fleets.\n
**Telecoms.** To process and analyze massive network performance data volumes and generate unique customer usage insights. \n
**Sustainability & climate resilience.** To overcome the processing limitations and costs associated with handling and visualizing large raster datasets.\n
**Geomarketing and Advertising.** To optimize high volume marketing campaigns by locating customers & prospects, and understanding temporal patterns.""")

# ------ Visualisation 3 ---------
st.divider()
st.subheader("Taxi pickups")
@st.cache_resource(ttl="4d")
def get_df_3(h3_resolut_3: int) -> pd.DataFrame:
    return session.sql(f'select h3_point_to_cell_string(pickup_location, {h3_resolut_3}) as h3, count(*) as count\n'\
                       'from snowpublic.streamlit.h3_ny_taxi_rides\n'\
                       'where 2 = 2\n'\
                       'group by 1\n').to_pandas()
@st.cache_resource(ttl="4d")
def get_quantiles_3(df_column: pd.Series, quantiles: List) -> pd.Series:
    return df_column.quantile(quantiles)

@st.cache_resource(ttl="4d")
def get_color_3(df_column: pd.Series, colors: List, vmin: int, vmax: int, index: pd.Series) -> pd.Series:
    color_map = cm.LinearColormap(colors, vmin=vmin, vmax=vmax, index=index)
    return df_column.apply(color_map.rgb_bytes_tuple)

@st.cache_resource(ttl="4d")
def get_layer_3(df: pd.DataFrame) -> pdk.Layer:
    return pdk.Layer("H3HexagonLayer", 
                     df, 
                     get_hexagon="H3",
                     get_fill_color="COLOR", 
                     get_line_color="COLOR",
                     get_elevation="COUNT/50000",
                     auto_highlight=True,
                     elevation_scale=50,
                     pickable=True,
                     elevation_range=[0, 300],
                     extruded=True,
                     coverage=1,
                     opacity=0.3)
   
col1, col2 = st.columns(2)
with col1:
    h3_resolut_3 = st.slider(
        "H3 resolution  ",
        min_value=6, max_value=9, value=7)

with col2:
    style_option_t_3 = st.selectbox("Style schema ",
                                ("Contrast", "Snowflake"), 
                                index=0)

df_3 = get_df_3(h3_resolut_3)

if style_option_t_3 == "Contrast":
    quantiles_3 = get_quantiles_3(df_3["COUNT"], [0, 0.25, 0.5, 0.75, 1])
    colors_3 = ['gray','blue','green','yellow','orange','red']
    st.image('./img/gradient_c.png')
if style_option_t_3 == "Snowflake":
    quantiles_3 = get_quantiles_3(df_3["COUNT"], [0, 0.33, 0.66, 1])
    colors_3 = ['#666666', '#24BFF2', '#126481', '#D966FF']
    st.image('./img/gradient_sf.jpg')

df_3['COLOR'] = get_color_3(df_3['COUNT'], colors_3, quantiles_3.min(), quantiles_3.max(), quantiles_3)
layer_3 = get_layer_3(df_3)

st.pydeck_chart(pdk.Deck(map_provider='carto',  map_style='light',
    initial_view_state=pdk.ViewState(
        latitude=40.74258515841464,
        longitude=-73.98452997207642, pitch=45, zoom=8),
        tooltip={
            'html': '<b>Pickups:</b> {COUNT}',
             'style': {
                 'color': 'white'
                 }
            },
    layers=[layer_3]))

# ------ Visualisation 3 End ---------

st.divider()
st.subheader("Network coverage")
# ------ Visualisation 4 ---------
@st.cache_resource(ttl="4d")
def get_df_4(resolution: int) -> pd.DataFrame:
    return session.sql(f'select h3_latlng_to_cell_string(lat, lon, {resolution}) as h3, count(*) as count\n'\
                       'from OPENCELLID.PUBLIC.RAW_CELL_TOWERS\n'\
                        'where mcc between 310 and 316\n'\
                            'group by 1').to_pandas()

@st.cache_resource(ttl="4d")
def get_quantiles_4(df_column: pd.Series, quantiles: List) -> pd.Series:
    return df_column.quantile(quantiles)

@st.cache_resource(ttl="4d")
def get_color_4(df_column: pd.Series, colors: List, vmin: int, vmax: int, index: pd.Series) -> pd.Series:
    color_map = cm.LinearColormap(colors, vmin=vmin, vmax=vmax, index=index)
    return df_column.apply(color_map.rgb_bytes_tuple)

@st.cache_resource(ttl="4d")
def get_layer_4(df: pd.DataFrame) -> pdk.Layer:
    return pdk.Layer("H3HexagonLayer", 
                     df, 
                     get_hexagon="H3",
                     get_fill_color="COLOR", 
                     get_line_color="COLOR",
                     get_elevation="COUNT",
                     auto_highlight=True,
                     elevation_scale=50,
                     pickable=True,
                     elevation_range=[0, 3000],
                     extruded=False,
                     coverage=1,
                     opacity=0.5)
    
col1, col2 = st.columns(2)

with col1:
    h3_resolution_4 = st.slider("H3 resolution     ", min_value=2, max_value=7, value=7)

with col2:
    style_option_4 = st.selectbox("Style schema     ", ("Contrast", "Snowflake"), index=0)

df_4 = get_df_4(h3_resolution_4)

if style_option_4 == "Contrast":
    quantiles_4 = get_quantiles_4(df_4["COUNT"], [0, 0.25, 0.5, 0.75, 1])
    colors_4 = ['gray','blue','green','yellow','orange','red']
    st.image('./img/gradient_c.png')
if style_option_4 == "Snowflake":
    quantiles_4 = get_quantiles_4(df_4["COUNT"], [0, 0.33, 0.66, 1])
    colors_4 = ['#666666', '#24BFF2', '#126481', '#D966FF']
    st.image('./img/gradient_sf.jpg')

df_4['COLOR'] = get_color_4(df_4['COUNT'], colors_4, quantiles_4.min(), quantiles_4.max(), quantiles_4)
layer_4 = get_layer_4(df_4)

st.pydeck_chart(pdk.Deck(map_provider='carto', map_style='light',
    initial_view_state=pdk.ViewState(
        latitude=38.51405689475766,
        longitude=-96.50284957885742, zoom=3),
                         tooltip={
        'html': '<b>Cell towers:</b> {COUNT}',
        'style': {
            'color': 'white'
        }
    },
    layers=[layer_4]))

# ------ Visualisation 6 End ---------
st.divider()

st.subheader("Login locations of Snowflake customers ")

@st.cache_resource(ttl="4d")
def get_df_5(resolution: int) -> pd.DataFrame:
    return session.sql(f'select * from snowpublic.streamlit.h3_ip_webinar').to_pandas()

@st.cache_resource(ttl="4d")
def get_quantiles_5(df_column: pd.Series, quantiles: List) -> pd.Series:
    return df_column.quantile(quantiles)

@st.cache_resource(ttl="4d")
def get_color_5(df_column: pd.Series, colors: List, vmin: int, vmax: int, index: pd.Series) -> pd.Series:
    color_map = cm.LinearColormap(colors, vmin=vmin, vmax=vmax, index=index)
    return df_column.apply(color_map.rgb_bytes_tuple)

@st.cache_resource(ttl="4d")
def get_layer_5(df: pd.DataFrame) -> pdk.Layer:
    return pdk.Layer("H3HexagonLayer", 
                     df, 
                     get_hexagon="H3",
                     get_fill_color="COLOR", 
                     get_line_color="COLOR",
                     get_elevation="COUNT/200",
                     auto_highlight=True,
                     elevation_scale=45,
                     pickable=True,
                     elevation_range=[0, 3000],
                     extruded=True,
                     coverage=1,
                     opacity=0.5)
    
col1, col2 = st.columns(2)

with col1:
    h3_resolution_5 = st.slider("H3 resolution       ", min_value=1, max_value=3, value=2)

with col2:
    style_option_5 = st.selectbox("Style schema       ", ("Contrast", "Snowflake"), index=0)

df_5 = get_df_5(h3_resolution_5)

if style_option_5 == "Contrast":
    quantiles_5 = get_quantiles_5(df_5["COUNT"], [0, 0.25, 0.5, 0.75, 1])
    colors_5 = ['gray','blue','green','yellow','orange','red']
    st.image('./img/gradient_c.png')
if style_option_5 == "Snowflake":
    quantiles_5 = get_quantiles_5(df_5["COUNT"], [0, 0.33, 0.66, 1])
    colors_5 = ['#666666', '#24BFF2', '#126481', '#D966FF']
    st.image('./img/gradient_sf.jpg')

df_5['COLOR'] = get_color_5(df_5['COUNT'], colors_5, quantiles_5.min(), quantiles_5.max(), quantiles_5)
layer_5 = get_layer_5(df_5)

st.pydeck_chart(pdk.Deck(map_provider='carto', map_style='light',
    initial_view_state=pdk.ViewState(
        latitude=38.51405689475766,
        longitude=-96.50284957885742, pitch=50, zoom=3),
        layers=[layer_5]))
