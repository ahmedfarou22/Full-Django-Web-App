import requests, os, sys
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import datetime


class DataExtraction:
    def __init__(self):
        self.url = "https://e4ftl01.cr.usgs.gov/MOLT/MOD16A2.006/"
        self.latest_file = None
        self.latest_date = None
        self.use_latest = False
        self.latest_url = "https://e4ftl01.cr.usgs.gov/MOLT/MOD16A2.006/"
        self.needed_files = []

    def julian_std(self):
        """
        Convert a Julian date to standard.
        """
        date = datetime.datetime.strptime(self.latest_date[2:], "%y%j")
        return date.strftime("%Y.%m.%d")

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
        self.latest_date = self.latest_file.split(".")[1][1:]
        os.chdir(cwd)

    def get_latest_url(self):
        req = requests.get(self.url)
        soup = BeautifulSoup(req.content, "lxml")
        latest = soup.find_all("a")[-1].get("href")
        if self.julian_std() == latest[:-1]:
            self.use_latest = True
        else:
            self.latest_url = self.latest_url + latest

            req = requests.get(self.latest_url)
            needed = ["h20v05", "h20v06", "h21v06"]

            soup = BeautifulSoup(req.content, "lxml")
            latest = [
                link.get("href")
                for link in soup.find_all("a")
                if link.get("href").endswith(".hdf")
            ]
            self.needed_files = [
                link for link in latest if link.split(".")[-4] in needed
            ]

    def save_latest_hdf(self):
        """
        Save the latest HDF files to the current directory.
        """
        self.get_latest_file()
        self.get_latest_url()
        if self.use_latest:
            return True
        else:

            for f in self.needed_files:
                req = requests.get(
                    self.latest_url + f,
                    stream=True,
                )
                file_name = (
                    f.split(".")[0]
                    + "."
                    + f.split(".")[1]
                    + "."
                    + f.split(".")[2]
                    + "."
                    + f.split(".")[-1]
                )
                with open(f"{file_name}", "wb") as hdf:
                    for chunk in req.iter_content(chunk_size=1024):
                        if chunk:
                            hdf.write(chunk)


if __name__ == "__main__":
    de = DataExtraction()
    de.save_latest_hdf()
