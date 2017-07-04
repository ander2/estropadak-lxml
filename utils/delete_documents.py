import couchdb

couch = couchdb.Server('http://admin:admin123@127.0.0.1:5984')
db = couch['estropadak']
docs = [ "3e2d2d934eb4fa4c18fe263f90009bd4", "3e2d2d934eb4fa4c18fe263f9000a432", "3e2d2d934eb4fa4c18fe263f9000a4bd", "3e2d2d934eb4fa4c18fe263f9000a954", "3e2d2d934eb4fa4c18fe263f9000ad5c", "3e2d2d934eb4fa4c18fe263f9000bb7c", "3e2d2d934eb4fa4c18fe263f9000bdc9", "3e2d2d934eb4fa4c18fe263f9000bec3", "3e2d2d934eb4fa4c18fe263f9000c210", "3e2d2d934eb4fa4c18fe263f9000c781", "3e2d2d934eb4fa4c18fe263f9000d23f", "3e2d2d934eb4fa4c18fe263f9000d7de", "3e2d2d934eb4fa4c18fe263f9000e1b0"]

for id in docs:
    try:
        doc = db[id]
        db.delete(doc)
    except:
        print("Cannot delete {}".format(id))
