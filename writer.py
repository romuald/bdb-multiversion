from common import *

set_trace()
txn = env.txn_begin(flags=0)
cursor = db.cursor(txn=txn)
print cursor.set_range('r')
cursor.delete()
cursor.close()
txn.commit()

