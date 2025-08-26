import binascii
head = binascii.hexlify(open("data_source/ai_file.zip", "rb").read(4))
print(head)  # 1f8b... → gzip, 78?? → zlib, 기타 → raw/다른 형식
