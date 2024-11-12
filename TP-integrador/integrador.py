import sys
from miel_scraper import MielScraper

if len(sys.argv) != 3:
    print("Error, cantidad de argumentos invalido")
    exit(1)

ms = MielScraper(sys.argv[1], sys.argv[2])

ms.login()
ms.get_subject_links()
ms.download_files()