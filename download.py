from fmiopendata.lightning import Lightning
import datetime
import csv
from fmiopendata.wfs import download_stored_query


def main():
    init_csv()
    start_date = datetime.date(2024, 5, 20)
    end_date = start_date + datetime.timedelta(weeks=2)
    dates = split_to_weeks(start_date, end_date)
    arg_list = format_args(dates)
    for args in arg_list:
        print(args)
        obs = download(args=args)
        write_obs(obs)


def split_to_weeks(start_date: datetime.date, end_date: datetime.date):
    dates = []
    date = start_date
    addition = datetime.timedelta(7)
    while date + addition < end_date:
        date = date + addition
        dates.append(date)
    dates.append(end_date)
    return dates


def format_args(dates: list[datetime.date]):
    arg_list = []
    for date in dates:
        start_date = date - datetime.timedelta(days=7)
        end_date = date - datetime.timedelta(days=1)
        args = [
            f"starttime={start_date}T00:00:00Z",
            f"endtime={end_date}T23:59:59Z",
        ]
        arg_list.append(args)

    return arg_list


def download(args) -> Lightning:
    lightnings = download_stored_query(
        "fmi::observations::lightning::multipointcoverage",
        args=args,
    )
    return lightnings


def init_csv():
    with open("lightnings.csv", "w", newline="") as file:
        writer = csv.writer(file)
        header = ["time", "peak_current", "latitude", "longitude"]
        writer.writerow(header)


def write_obs(obs):
    zipped_obs = zip(obs.times, obs.peak_current, obs.latitudes, obs.longitudes)
    print(f"writing {len(obs.times)} lightnings\n")

    with open("lightnings.csv", "a", newline="") as file:
        writer = csv.writer(file)
        for time, peak_current, lat, lon in zipped_obs:
            row = [
                int(time.timestamp()),
                abs(peak_current),
                lat,
                lon,
            ]
            writer.writerow(row)


if __name__ == "__main__":
    main()
