import click
import shutil
import os
import time
import sys
from partLib import PartLibrary, loadJlcTable, getLcscExtra, obtainCsrfTokenAndCookies
from datatables import buildtables
from config import CSV_FILE

def getLibrary(source, output):
    """
    Download library inside OUTPUT (JSON format) based on SOURCE (csv table
    provided by JLC PCB).

    Cou can specify previously downloaded library as a cache to save requests to
    fetch LCSC extra data.
    """
    lib = PartLibrary()

    with open(source, newline="") as f:
        jlcTable = loadJlcTable(f)

    # Make copy of the output in case we make a mistake
    if os.path.exists(output):
        shutil.copy(output, output + ".bak")

    for i, component in enumerate(jlcTable.values()):
        lib.addComponent(component)
    lib.save(output)


def listcategories(libraryfilename):
    """
    Print all categories from library specified by LIBRARYFILENAMEto standard
    output
    """
    lib = PartLibrary(libraryfilename)
    for c, subcats in lib.categories().items():
        print(f"{c}:")
        for s in subcats:
            print(f"  {s}")


def listattributes(libraryfilename):
    """
    Print all keys in the extra["attributes"] arguments from library specified by
    LIBRARYFILENAMEto standard output
    """
    keys = set()
    lib = PartLibrary(libraryfilename)
    for subcats in lib.lib.values():
        for parts in subcats.values():
            for data in parts.values():
                if "extra" not in data:
                    continue
                extra = data["extra"]
                attr = extra.get("attributes", {})
                if not isinstance(attr, list):
                    for k in extra.get("attributes", {}).keys():
                        keys.add(k)
    for k in keys:
        print(k)
