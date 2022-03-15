from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

# 单线程
server = SimpleJSONRPCServer(('localhost', 8080))
server.register_function(lambda x, y: x + y, 'add')
server.serve_forever()