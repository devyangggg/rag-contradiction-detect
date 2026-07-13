#Ill be making a design choice here. For now the project is kinda small so not alot of crazy tech is requied and with a heavy heart
#i wont be using K means or ANN becuase of their own shortcoming and stuff. my data is not that big and im choosing to
#dot product them to get results. For applications bigger than right now, i will upgade to a K-Mean but rn because choosing a wrong k
#can mess stuff up, i will not go down that rabbit hole

import numpy as np
import lancedb

db = lancedb.connect("./my_db")

tbl = db.open_table("my_vectors").to_pandas()

matrix1 = np.stack(tbl["vector"].values)

norm = np.linalg.norm(matrix1, axis=1, keepdims=True)

matrix1 = matrix1 / norm

matrix2 = matrix1.T

res = np.dot(matrix1,matrix2)
#basically how similar sentence i and sentence j are in the matrix correponding to res[i][j]

file_names = tbl["file_name"].to_numpy()
file_mask = file_names[:, None] == file_names[None, :]

res_final = np.where(file_mask, res, -1)
np.fill_diagonal(res_final, -1)

row_ids = tbl["row_key"].values

thresh = 0.85

filtered_res = res_final > thresh

# matches = np.array([])
# for i in range(len(res_final)):
#     for j in range(len(res_final)):
#         if res_final[i][j] > thresh:
#             matches.append((row_ids[i], row_ids[j], res_final[i][j]))

i_idx, j_idx = np.where(filtered_res)

matches = []
for i, j in zip(i_idx, j_idx):
    matches.append((row_ids[i], row_ids[j], res_final[i][j]))



print(matches)




