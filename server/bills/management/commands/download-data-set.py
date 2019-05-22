import os
import csv
import shutil

from django.core.files import File
from django.core.management import BaseCommand

from bills.models import Bill


def run_gdrive_tool(command):
    gdrive_tool_path = os.path.normpath(os.path.dirname(__file__) + "/../../../tools/gdrive-windows-x64.exe")
    # gdrive_tool_path = "gdrive"
    print(gdrive_tool_path + " " + command)
    ret = os.system(gdrive_tool_path + " " + command)
    print(ret)


def run_in_tmp_folter(func):
    try:
        shutil.rmtree("tmp")
    except:
        pass
    os.mkdir("tmp")
    os.chdir("tmp")
    func()
    os.chdir("..")
    files = os.listdir("tmp")
    file = files[0]
    return "tmp/" + file


def download_file_from_gdrive(id):
    return run_in_tmp_folter(lambda: run_gdrive_tool('download "' + id + '"'))


def download_spreadsheet_as_csv(id):
    return run_in_tmp_folter(lambda: run_gdrive_tool('export --mime text/csv "' + id + '"'))


FEATURES = ["us_district", "us_seal_color", "us_signature", "us_star", "us_series", "il_number_color"];


def sync():
    csv_file = download_spreadsheet_as_csv("1-JD7zf6NyprMBsd1nOo34cCpYql24x0RndWDCgI6f6U")
    print("file is here", csv_file)
    shutil.copyfile(csv_file, "tmp.csv")
    with open("tmp.csv", "r") as csv_file:
        reader = csv.reader(csv_file)
        first_skip = True
        for row in reader:
            print(row)
            if first_skip:
                first_skip = False
                continue
            try:
                print(row)
                (back_url,  # A
                 front_url,  # B
                 heritage,  # C
                 ebay,  # D
                 pmg,  # E
                 cat,  # F
                 name,  # G
                 num,  # H
                 billOrCoin,  # I
                 image_id,  # J,
                 ) = row[0:10]
                if len(back_url.split('/')) < 5 or len(front_url.split('/')) < 5:
                    print("empty row", row)
                    continue
                print("Search", cat)
                features = row[10:]
                try:
                    bill = Bill.objects.get(catalog=cat)
                    print("already exists")
                except Bill.DoesNotExist:
                    print("creating new")
                    bill = Bill(catalog=cat)
                bill.name = name
                bill.heritage_link = heritage
                bill.ebay_link = ebay
                bill.pmg_link = pmg

                back_id = back_url.split("/")[5]
                tmp_file = download_file_from_gdrive(back_id)
                bill.back.save(cat + "_back.jpg", File(open(tmp_file, "rb")))

                front_id = front_url.split("/")[5]
                tmp_file = download_file_from_gdrive(front_id)
                bill.front.save(cat + "_front.jpg", File(open(tmp_file, "rb")))

                bill.is_coin = billOrCoin == "Coin"
                bill.image_id = image_id
                feature_dict = {}
                for i in range(len(features)):
                    feature = features[i]
                    if feature:
                        value = feature
                        if value == "FALSE":
                            value = False
                        if value == "TRUE":
                            value = True
                        feature_dict[FEATURES[i]] = value
                print(feature_dict)
                bill.features = feature_dict
                bill.save()
            except Exception as e:
                print("Error parsing row", e)

    csv_file.close()


class Command(BaseCommand):
    help = 'Download data set from drive'

    def handle(self, *args, **options):
        sync()
