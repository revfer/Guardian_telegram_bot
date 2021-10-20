import pyqiwi
from config import QIWI_TOKEN
import datetime
from dateutil.tz import tzoffset


def get_last_history(num=20):
    wallet = pyqiwi.Wallet(token=QIWI_TOKEN, number='phone_number')
    spis = []
    for i in wallet.history(rows=num)['transactions']:
        a = eval(str(i))
        # print(a)
        spis.append([a['comment'], float(a['raw']['sum']['amount']), a['raw']['type'], a['raw']['status'],
                     a['raw']['statusText'], int(a['raw']['sum']['currency'])])
    return list(filter(lambda x: x[2] == 'IN' and x[3].lower() == x[4].lower() == 'success', spis))


# a['raw']['sum']['currency']
# Рубль 643; доллар 840; гривны 980

if __name__ == '__main__':
    print(get_last_history())
