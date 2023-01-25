
# pencryptor: Pack files and encrypt them with 7zip

remove file structure and only care about files

compress all files into 7zip archive with encryption

then, split the archive into 3 parts:

1. header part
2. content part in the middle
3. tail part

the (2.) content part will take up majority of the size

and it is hard to decrypt & extract due to missing file header & tail





