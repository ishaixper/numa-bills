import os
import csv
import shutil

from django.core.files import File
from django.core.management import BaseCommand

from bills.models import Bill


def run_gdrive_tool(command):

    #gdrive_tool_path = os.path.normpath(os.path.dirname(__file__) + "/../../../tools/gdrive-windows-x64.exe")
    gdrive_tool_path = "gdrive"
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
            print(row)
            (back_url, front_url, heritage, ebay, pmg, cat, name, num, billOrCoin) = row
            if len(back_url.split('/')) < 5 or len(front_url.split('/')) < 5:
                print("empty row", row)
                continue
            print("Search", cat)
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
            bill.save()

    csv_file.close()


class Command(BaseCommand):
    help = 'Download data set from drive'

    def handle(self, *args, **options):
        sync()
