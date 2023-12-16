import funcs
import argparse
import inspect
import time


parser = argparse.ArgumentParser(
    description="coki es una CLI para consultar precios en cocos"
)
parser.add_argument(
    "--ticker", "-T", help="Ticker a filtrar en el listado de ordenes", default="ALL"
)
parser.add_argument(
    "--filtro",
    "-F",
    help="Filtro de estado a aplicar en el listado de ordenes",
    default="cancelado",
    choices=["cancelado", "ejecutado", "mercado"],
)


parser.add_argument(
    "--refresh",
    "-R",
    help="Intervalo de actualización de los precios (en segundos)",
    default=30,
)


args = parser.parse_args()

ticker = args.ticker.upper()
filtro = args.filtro.lower()
refresh = args.refresh

account_id = open("account_id.txt", "r").read()

if refresh < 1:
    funcs.gen_table_orders(account_id, ticker=ticker, filtro=filtro)
else:
    while True:
        funcs.gen_table_orders(account_id, ticker=ticker, filtro=filtro)
        time.sleep(refresh)
