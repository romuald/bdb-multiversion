from common import *

set_trace()
cursor = db.cursor(flags=DB_TXN_SNAPSHOT)
print cursor.set_range('r')
print cursor.next()
cursor.close()

