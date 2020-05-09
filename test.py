import index_inverse as ii

index = ii.index_inverse(score = "log")
index.compute()

print(index.sort_tf_idf("OCaml"))
print(index.ten_first("OCaml"))
