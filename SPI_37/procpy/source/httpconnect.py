import httplib
import socket
host = socket.gethostname()
print host
conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
r1 = conn.getresponse()
print r1.status, r1.reason                                                            