# importing pandas as pd
import ntpath

import pandas as pd
from datetime import datetime
import os
from pathlib import Path
from Meteostation.main.models import *


def main():
    # Read and store content
    # of an excel file
    path = "львів/2012-1.xlsx"
    read_file = pd.read_excel(path)

    # Write the dataframe object
    # into csv file
    read_file.to_csv("Temp.csv", index=None, header=True)

    # read csv file and convert
    # into a dataframe object
    df = pd.DataFrame(pd.read_csv("львів/Temp.csv"))


    # Clear the file
    # f = open("Temp.csv", "w")
    # f.close()
    # if os.path.isfile(path):
    #     os.remove(path)

    # show the dataframe
    print(df)
    # filename = os.ntpath.basename(path)
    filename = Path(path).stem
    # print(df.iloc[10:15, 7])

    def create_obj(row):
        date = datetime.strptime(f"{filename}-{row[0]} {row[1]}", '%Y-%-m-%d %H:%M:%S')
        temperature = int(row[2])
        directions = Direction.objects.get
        direction = directions(direction="Calm")
        if row[3] == "Переменный":
            direction = directions(direction="Variable")
        elif row[3] == "Северный":
            direction = directions(direction="North")
        elif row[3] == "С-В":
            direction = directions(direction="North-East")
        elif row[3] == "Восточный":
            direction = directions(direction="East")
        elif row[3] == "Ю-В":
            direction = directions(direction="South-East")
        elif row[3] == "Южный":
            direction = directions(direction="South")
        elif row[3] == "Ю-З":
            direction = directions(direction="South-West")
        elif row[3] == "Западный":
            direction = directions(direction="West")
        elif row[3] == "С-З":
            direction = directions(direction="North-West")
        velocity = int(row[4])
        code = None
        if f"{row[5]}" == "nan":
            code = "CL"
        else:
            code = row[5]

        clouds = int(row[6])
        visibility = None
        try:
            visibility = datetime.strptime(row[7], '%Y-%m-%d %H:%M:%S')
            visibility = float(f"{visibility.day}.{visibility.month}")
        except ValueError as e:
            visibility = float(row[7])
        humidity = int(row[8])
        pressure = int(row[9])
        lower_limit = int(row[10])
        Data.objects.create(date=date, temperature=temperature, direction=direction,
                            velocity=velocity, weather_code=code, cloud_amount=clouds,
                            visibility_range=visibility, humidity=humidity, atmo_pressure=pressure,
                            lower_cloud_limit=lower_limit)

    obj = df.iloc[10, 7]
    print(type(df.iloc[10, 7]).__name__)
    result = None
    try:
        result = datetime.strptime(obj, '%Y-%m-%d %H:%M:%S')
        result = float(f"{result.day}.{result.month}")
    except ValueError as e:
        result = float(obj)
    print(result)
    print(type(result).__name__)

    for i in range(11):
        print(f"{i}. value:{df.iloc[0, i]};{type(df.iloc[0, i]).__name__}")


if __name__ == '__main__':
    main()
