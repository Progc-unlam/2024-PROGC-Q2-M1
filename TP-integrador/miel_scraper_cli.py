import sys
from miel_scraper import MielScraper

if len(sys.argv) != 3:
    print("Uso: python3 miel_scraper_cli.py <usuario> <contraseña>")
    exit(1)

ms = MielScraper()

ms.login(sys.argv[1], sys.argv[2])
ms.get_files_to_download()
ms.download_files()
