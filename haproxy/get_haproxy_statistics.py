import requests
import csv

def get_statistics_from_url(url, user, password):
    r = requests.get(url, auth=(user, password))
    data = r.content.lstrip('# ')
    return csv.DictReader(data.splitlines())
