#Ill be making a design choice here. For now the project is kinda small so not alot of crazy tech is requied and with a heavy heart
#i wont be using K means or cosine sim becuase of their own shortcoming and stuff. my data is not that big and im choosing to
#dot product them to get results. For applications bigger than right now, i will upgade to a K-Mean but rn because choosing a wrong k
#can mess stuff up, i will not go down that rabbit hole


import lancedb

db = lancedb.connect("./my_db")

# Open a table and view its contents
tbl = db.open_table("my_vectors")







