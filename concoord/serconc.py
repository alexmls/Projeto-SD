# !/usr/bin/python
# Autor: Alexandre Mariano, Murilo Marques, Guilherme Campos


class Serconc:
    def __init__(self):
        self.dty = {}

    def create(self, key, value):
        if self.dty.has_key(key):
            print "Client tried to create a key that's already exists!!!"
            return "Key already exists!!!"
        else:
            self.dty[key] = value
            print "Created key: ", key, ":", self.dty[key]
            return "Created!!!"

    def retrieve(self, key):
        if self.dty.has_key(key):
            print "Key retrieved: ", key, ":", self.dty[key]
            return self.dty.get(key)
        else:
            print "Client tried to retrieve a key nonexistent!!!"
            return "Key dont exist!!!"

    def update(self, key, value):
        if self.dty.has_key(key):
            self.dty[key] = value
            print "Key updated: ", key, ":", self.dty[key]
            return "Updated!!!"
        else:
            self.dty[key] = value
            print "Not found... New register created: ", self.dty[key]
            return "Not found... New register created!!!"

    def delete(self, key):
        if self.dty.has_key(key):
            print "Key deleted: ", key, ":", self.dty[key]
            return self.dty.pop(key)
        else:
            print "Client tried to retrieve a key nonexistent!!!"
            return "Key not found to delete!!!"

    def charge(stg):  # execute the dictionary operations in stg
        flg, content = stg.split('.')  # extract the flag and content from string received
        key, value = content.split(',')  # extract the key and the string from content

        if flg == '1':
            if key not in dty:
                dty[key] = value
            else:
                pass
        elif flg == '2':
            pass
        elif flg == '3':
            if key not in dty:
                dty[key] = value
            else:
                pass
        elif flg == '4':
            if key not in dty:
                pass
            else:
                dty.pop(key)