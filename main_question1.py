import plotly.express as px 
import plotly.graph_objects as go
from utils.sqlite_utils import SQLiteDB
from utils.analysis_utils import ask_times, insertHours_button, generate_times
import pandas as pd

def main():
    try:
        # connect to db
        sqlite_db = SQLiteDB(database='/Users/marcosmorenoblanco/Documents/bicing/bicing.db')
        query = "SELECT * From bicing"
        # import data from db through query
        results = sqlite_db.retrieve_as_df(query=query)

        # timestamp to datetime since it is saved as string
        results['timestamp'] = pd.to_datetime(results['timestamp'], infer_datetime_format=True)

        # timestamp as index to filter through it
        results.set_index('timestamp', inplace=True)

        # hours to check in between
        time1, time2 = ask_times()
        times = generate_times(time1, time2)

        # map
        fig = go.Figure()
        for i, time in enumerate(times[:-1]):
            if (i == 0):
                fig = px.set_mapbox_access_token(open(".mapbox_token").read())
                fig = px.scatter_mapbox(results.between_time(time, times[i+1]), lat="latitude", lon="longitude", color="empty_slots", size="free_bikes", hover_name="name",
                mapbox_style = 'streets', color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=12)
            else:
                fig2 = px.set_mapbox_access_token(open(".mapbox_token").read())
                fig2 = px.scatter_mapbox(results.between_time(time, times[i+1]), lat="latitude", lon="longitude", color="empty_slots", size="free_bikes", hover_name="name",
                mapbox_style = 'streets', color_continuous_scale=px.colors.cyclical.IceFire, size_max=20, zoom=12)
                fig.add_trace(fig2.data[0])
        insertHours_button(fig, times)
        fig.update_layout(
        autosize=False,
        width=1700,
        height=1000,)
        fig.show()

    except Exception as ex:
        print(ex)

if __name__ == "__main__":
    main()