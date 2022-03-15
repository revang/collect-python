import xmlrpc.client

server = xmlrpc.client.ServerProxy("http://localhost:8000")

print(server.add(1, 2))
print(server.add1(1, 2))
print(server.pow(1, 2))
print(server.multiply(1, 2))
print(server.system.listMethods())