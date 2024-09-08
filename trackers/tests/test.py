import pandas as pd
import json

def interpolate_shuttle_tracking(json_path):
    # Load the JSON tracking data
    with open(json_path, 'r') as file:
        tracking_data = json.load(file)

    # Extract the x and y coordinates for each frame from the JSON data
    shuttle_coordinates_frames = [
        (frame_data['x_center'], frame_data['y_center'], frame_data['smoothened_speed'])
        for frame_data in tracking_data.values()
    ]

    print(len(shuttle_coordinates_frames))

    # Convert the coordinates into a pandas DataFrame
    df_shuttle_positions = pd.DataFrame(shuttle_coordinates_frames, columns=['x_center', 'y_center', 'smoothened_speed'])

    # Interpolate missing values
    df_shuttle_positions = df_shuttle_positions.interpolate(method='linear')
    df_shuttle_positions = df_shuttle_positions.bfill()

    # Convert the interpolated DataFrame back to a list
    # interpolated_shuttle_coordinates = df_shuttle_positions.to_numpy().tolist()
    shuttle_positions_dict = df_shuttle_positions.to_dict(orient='index')

    return shuttle_positions_dict

if __name__ == '__main__':
    # interpolated_shuttle_coordinates = interpolate_shuttle_tracking('../../result/shuttle_data/shuttle_data.json')
    # print(interpolated_shuttle_coordinates)
    pass