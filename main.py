import mysql.connector
import schedule
from datetime import datetime
import time

from webscraping.continente import get_continente
from webscraping.garrafeirasoares import get_garrafeira_soares
from webscraping.elingles import get_elingles
from prettytable import PrettyTable
x = PrettyTable()
x.field_names = ["EAN", "Store Name",  "HarvestYear", "Price", "Discount", "Currency", "Date", "Location"]
sql_EAN_Query = "SELECT EAN FROM wines"
sql_NAME_Query = "SELECT Name FROM wines"
sql_insert_statement = """INSERT INTO scrape (EAN, StoreName, HarvestYear, Price, Discount, Currency, Date, Location) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

def time_get():
   now = datetime.now()
   current_time = now.strftime("%H:%M:%S")
   return current_time

def main():
  conn = mysql.connector.connect(host='34.175.219.22', database='wines', user='root', password='root')
  cursor = conn.cursor()
  cursor.execute(sql_EAN_Query)
  eans = cursor.fetchall()
  cursor.execute(sql_NAME_Query)
  names = cursor.fetchall()

  y = -1
  for ean in eans:
    y = y + 1
    print("Scraping Wine \"" + str(names[y][0]) + "\"...")
    continente = get_continente(ean[0])
    x.add_row(continente)
    cursor.execute(sql_insert_statement, continente)
    soares = get_garrafeira_soares(ean[0])
    x.add_row(soares)
    cursor.execute(sql_insert_statement, soares)
    elingles = get_elingles(ean[0])
    x.add_row(elingles)
    cursor.execute(sql_insert_statement, elingles)
    print(x)
    x.clear_rows()
  print("Scrapping finished successfully!")
  conn.commit()
  print("Database upload completed!")
  cursor.close()
  conn.close()

print("Scraper started to run at " + time_get() + "...")
schedule.every(60).minutes.do(main)
while True:
    time.sleep(3601)
    print(time_get() + " - Running Scraper...")
    schedule.run_pending()
    print(time_get() + " - Finished Scrapping...")
