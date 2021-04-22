from cassandra.cluster import Cluster,Session,ResponseFuture,Event
from cassandra.auth import PlainTextAuthProvider
from cassandra.query import SimpleStatement


'''
cassandra自动分页 功能 测试
'''
#认证
auth_provider = PlainTextAuthProvider(username = "cassandra",password = "cassandra")

cluster = Cluster(['10.0.0.61'],auth_provider = auth_provider ,protocol_version=3)

session = cluster.connect("eo_osclassin")
query = "select * from eeo_user_autocheck"


class PagedResultHandler(object):

    def __init__(self, future):
        self.error = None
        self.finished_event = Event()
        self.future = future
        self.future.add_callbacks(
            callback=self.handle_page,
            errback=self.handle_err)

    def handle_page(self, rows):
        print("-----------------------")
        for row in rows:
            print(row.classid)
        # exit()

        if self.future.has_more_pages:
            self.future.start_fetching_next_page()
        else:
            self.finished_event.set()

    def handle_err(self, exc):
        self.error = exc
        self.finished_event.set()


statement = SimpleStatement(query,fetch_size=10)

# rows = session.execute(statement)

future = session.execute_async(statement)
# future = session.execute("SELECT * FROM eeo_user_autocheck")
handler = PagedResultHandler(future)
print("============")
handler.finished_event.wait()
print("===========00000000=")
if handler.error:
    raise handler.error