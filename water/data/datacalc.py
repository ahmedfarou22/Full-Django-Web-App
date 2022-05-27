from pyhdf.SD import SD, SDC
from .locations import *
import requests, os, sys
import rioxarray as rxr
import pandas as pd
from sentinelhub import SHConfig
from sentinelhub import (
    MimeType,
    CRS,
    BBox,
    SentinelHubRequest,
    DataCollection,
    bbox_to_dimensions,
)


class Environment:
    def __init__(self, crop: str, coords: tuple) -> None:
        self.crop = crop
        self.coords = coords
        self.soil = None
        self.region = None
        self.weather = None
        self.temp = None
        self.water_req = None
        self.tile = None
        self.latest_file = None
        self.latest_date = None

    def get_latest_file(self):
        """
        Get the latest HDF file from the directory.
        """
        cwd = os.getcwd()
        os.chdir(
            os.path.dirname(
                r"D:\Uni\Year_3\Semester_2\Web_Security\CW\course-work-silent-cyber-watch\django\water\data\data"
            )
        )
        all_hdf = []

        for x in os.listdir():
            if x.endswith(".hdf"):
                all_hdf.append(x)

        self.latest_file = max(all_hdf, key=os.path.getctime)
        self.latest_date = self.latest_file.split(".")[1]
        os.chdir(cwd)

    def get_coord_tile(self):
        """Get the MODIS tiles for the coordinates"""
        # City names used to differentiate tiles
        print(os.getcwd())
        self.get_latest_file()
        tanta = rxr.open_rasterio(
            "water\\data\\" + "MOD16A2." + self.latest_date + ".h20v05.hdf",
            masked=True,
        )
        faiom = rxr.open_rasterio(
            "water\\data\\" + "MOD16A2." + self.latest_date + ".h20v06.hdf",
            masked=True,
        )
        hurgh = rxr.open_rasterio(
            "water\\data\\" + "MOD16A2." + self.latest_date + ".h21v06.hdf",
            masked=True,
        )

        tanta_bounds = (
            (
                tanta.attrs["WESTBOUNDINGCOORDINATE"],
                tanta.attrs["NORTHBOUNDINGCOORDINATE"],
            ),
            (
                tanta.attrs["EASTBOUNDINGCOORDINATE"],
                tanta.attrs["SOUTHBOUNDINGCOORDINATE"],
            ),
        )
        faiom_bounds = (
            (
                faiom.attrs["WESTBOUNDINGCOORDINATE"],
                faiom.attrs["NORTHBOUNDINGCOORDINATE"],
            ),
            (
                faiom.attrs["EASTBOUNDINGCOORDINATE"],
                faiom.attrs["SOUTHBOUNDINGCOORDINATE"],
            ),
        )
        hurgh_bounds = (
            (
                hurgh.attrs["WESTBOUNDINGCOORDINATE"],
                hurgh.attrs["NORTHBOUNDINGCOORDINATE"],
            ),
            (
                hurgh.attrs["EASTBOUNDINGCOORDINATE"],
                hurgh.attrs["SOUTHBOUNDINGCOORDINATE"],
            ),
        )

        if (
            self.coords[0] >= tanta_bounds[0][0]
            and self.coords[1] <= tanta_bounds[0][1]
            and self.coords[0] <= tanta_bounds[-1][0]
            and self.coords[1] >= tanta_bounds[-1][1]
        ):
            self.tile = "tanta"
            self.tile_bounds = tanta_bounds
            self.file_name = "MOD16A2." + self.latest_date + ".h20v05.hdf"

        if (
            self.coords[0] >= faiom_bounds[0][0]
            and self.coords[1] <= faiom_bounds[0][1]
            and self.coords[0] <= faiom_bounds[-1][0]
            and self.coords[1] >= faiom_bounds[-1][1]
        ):
            self.tile = "faiom"
            self.tile_bounds = faiom_bounds
            self.file_name = "MOD16A2." + self.latest_date + ".h20v06.hdf"

        if (
            self.coords[0] >= hurgh_bounds[0][0]
            and self.coords[1] <= hurgh_bounds[0][1]
            and self.coords[0] <= hurgh_bounds[-1][0]
            and self.coords[1] >= hurgh_bounds[-1][1]
        ):
            self.tile = "hurgh"
            self.tile_bounds = hurgh_bounds
            self.file_name = "MOD16A2." + self.latest_date + ".h21v06.hdf"

    def get_coord_env(self) -> bool:
        """
        Determines the environment the coordinates belong to
        """
        for location in hum_semihum_locations:
            if (
                location[2] < self.coords[0] < location[0]
                and location[1] < self.coords[1] < location[3]
            ):
                self.soil = "humid"
                self.region = "semi humid"
                return True

        for location in dry_desert_locations:
            if (
                location[2] < self.coords[0] < location[0]
                and location[1] < self.coords[1] < location[3]
            ):
                self.soil = "dry"
                self.region = "desert"
                return True

        for location in hum_hum_locations:
            if (
                location[2] < self.coords[0] < location[0]
                and location[1] < self.coords[1] < location[3]
            ):
                self.soil = "humid"
                self.region = "humid"
                return True

        for location in dry_semiarid_locations:
            if (
                location[2] < self.coords[0] < location[0]
                and location[1] < self.coords[1] < location[3]
            ):
                self.soil = "dry"
                self.region = "semi arid"
                return True

        self.soil, self.region = self.get_closest_env()
        return True

    def get_closest_env(self) -> tuple:
        """
        If coordinates are not in one of allocated region boxes, this function gets closest box to the coordinates
        """
        closest_y = (hum_semihum_locations[0][0] + hum_semihum_locations[0][2]) / 2
        closest_x = (hum_semihum_locations[0][1] + hum_semihum_locations[0][3]) / 2
        closest = (closest_y, closest_x)
        soil = "humid"
        region = "semi humid"

        for location in hum_semihum_locations:
            center_y = (location[0] + location[2]) / 2
            center_x = (location[1] + location[3]) / 2
            center = (center_y, center_x)
            if (
                abs(center[0] - self.coords[0]) < abs(closest[0] - self.coords[0])
            ) and (abs(center[1] - self.coords[1]) < abs(closest[1] - self.coords[1])):
                closest = center
                soil = "humid"
                region = "semi humid"

        for location in dry_desert_locations:
            center_y = (location[0] + location[2]) / 2
            center_x = (location[1] + location[3]) / 2
            center = (center_y, center_x)
            if (
                abs(center[0] - self.coords[0]) < abs(closest[0] - self.coords[0])
            ) and (abs(center[1] - self.coords[1]) < abs(closest[1] - self.coords[1])):
                closest = center
                soil = "dry"
                region = "desert"

        for location in hum_hum_locations:
            center_y = (location[0] + location[2]) / 2
            center_x = (location[1] + location[3]) / 2
            center = (center_y, center_x)
            if (
                abs(center[0] - self.coords[0]) < abs(closest[0] - self.coords[0])
            ) and (abs(center[1] - self.coords[1]) < abs(closest[1] - self.coords[1])):
                closest = center
                soil = "humid"
                region = "humid"

        for location in dry_semiarid_locations:
            center_y = (location[0] + location[2]) / 2
            center_x = (location[1] + location[3]) / 2
            center = (center_y, center_x)
            if (
                abs(center[0] - self.coords[0]) < abs(closest[0] - self.coords[0])
            ) and (abs(center[1] - self.coords[1]) < abs(closest[1] - self.coords[1])):
                closest = center
                soil = "dry"
                region = "semi arid"
        return soil, region

    def get_weather_temp(self) -> bool:
        """
        Determines the weather based on the coordinates
        """
        req = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather?lat={self.coords[0]}&lon={self.coords[1]}&appid=a7eb75b45a4637587bbce3323469c5a1&units=metric"
        )
        data = req.json()
        w_id, t, w_speed = (
            data["weather"][0]["id"],
            data["main"]["temp"],
            data["wind"]["speed"],
        )

        if w_id == 800:
            self.weather = "sunny"
        if w_id in range(200, 700):
            self.weather = "rainy"
        elif w_id in range(801, 900):
            self.weather = "normal"

        if w_speed >= 8.9:
            self.weather = "windy"

        if t < 20:
            self.temp = 10
        elif t >= 20 and t < 30:
            self.temp = 20
        elif t >= 30 and t < 40:
            self.temp = 30
        elif t >= 40:
            self.temp = 40

        return True

    def get_prop(self) -> bool:
        """
        Gets all properties of the coordinates
        """
        self.get_coord_env()
        self.get_weather_temp()
        return True

    def get_water_req(self) -> bool:
        """
        Gets the water requirement of the field
        """
        self.get_prop()
        self.get_surplus()
        df = pd.read_csv("water/data/dataset.csv")
        self.water_req = df[
            (df["CROP"] == self.crop.upper())
            & (df["SOIL"] == self.soil.upper())
            & (df["REGION"] == self.region.upper())
            & (df["TEMPERATURE"] == self.temp)
            & (df["WEATHER"] == self.weather.upper())
        ]["WATER REQUIREMENT"].values[0]
        return True

    def get_pixel(self):
        """Gets the pixel value at the given coordinates"""

        init = (self.tile_bounds[0][0], self.tile_bounds[0][1])
        final = (self.tile_bounds[-1][0], self.tile_bounds[-1][1])
        xi = init[0]
        xf = final[0]

        yi = init[1]
        yf = final[1]

        ratio_x = (self.tile_bounds[0][0] - self.tile_bounds[1][0]) / 2400
        ratio_y = (self.tile_bounds[1][1] - self.tile_bounds[0][1]) / 2400

        x_pixel = abs(self.coords[0] - xi) / abs(ratio_x)
        y_pixel = abs(yi - self.coords[1]) / abs(ratio_y)

        return round(x_pixel), round(y_pixel)

    def get_moisture_index(self):
        """Gets moisture index from coordinates using Sentinelhub API"""

        # Add access token information
        config = SHConfig()
        config.instance_id = "41ce74e7-47e2-42ca-b46b-a62557820c6b"
        config.sh_client_id = "e0e1c34f-40c4-4b30-b13c-b5ba04306c19"
        config.sh_client_secret = "@BRp&@rc-|peI@fZey0_K]L9<,yB+}ROzE!5-A.k"

        # Adds coordinates to be used in the request
        plot_coords_wgs84 = [
            self.coords[0],
            self.coords[1],
            self.coords[0] + 0.002,
            self.coords[1] + 0.002,
        ]
        resolution = 130
        plot_bbox = BBox(bbox=plot_coords_wgs84, crs=CRS.WGS84)
        plot_size = bbox_to_dimensions(plot_bbox, resolution=resolution)
        items = plot_size[0] * plot_size[1]

        # Adds the request to the Sentinelhub API
        evalscript_all_bands = """
            //VERSION=3
            function setup() {
                return {
                    input: [{
                        bands: ["B8A","B11"],
                    }],
                    output: {
                        bands: 1,
                        sampleType: "FLOAT32"
                    }
                };
            }

            function evaluatePixel(sample) {
                return [(sample.B8A - sample.B11)/(sample.B8A + sample.B11)];
            }
        """

        request_all_bands = SentinelHubRequest(
            evalscript=evalscript_all_bands,
            input_data=[
                SentinelHubRequest.input_data(
                    data_collection=DataCollection.SENTINEL2_L1C,
                    time_interval=("2020-06-01", "2020-06-30"),
                )
            ],
            responses=[SentinelHubRequest.output_response("default", MimeType.TIFF)],
            bbox=plot_bbox,
            size=plot_size,
            config=config,
        )
        # Data saved for access later
        data = request_all_bands.get_data()
        # Average moisture index is calculated
        mi = (sum(data[0][-1]) + sum(data[0][0])) / items

        return mi

    def get_surplus(self):
        """Gets the surplus at the given wgs84 coordinates"""
        self.get_coord_tile()
        x_pixel, y_pixel = self.get_pixel()

        file = SD("water\\data\\" + self.file_name, SDC.READ)

        sds_obj = file.select("PET_500m")
        data = sds_obj.get()

        data = data * sds_obj.scale_factor
        PE = data[y_pixel, x_pixel]

        mi = self.get_moisture_index()
        self.surplus = abs(mi * PE / 100 * 1000 / 8)  # Surplus in ml/m2

    def parse_to_json(self) -> dict:
        """
        Parses the class to a json object
        """
        return {
            "crop": self.crop,
            "coords": self.coords,
            "soil": self.soil,
            "region": self.region,
            "weather": self.weather,
            "temp": self.temp,
            "water_req": self.water_req,
            "surplus": self.surplus,
        }
