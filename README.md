
# pencryptor: Pack files and encrypt them with 7zip

remove file structure and only care about files

compress all files into 7zip archive with encryption

then, split the archive into 3 parts:

1. header part
2. content part in the middle
3. tail part

the (2.) content part will take up majority of the size

and it is hard to decrypt & extract due to missing file header & tail

# Usage

```py
from pencryptor import PackEncryptor

pe = PackEncryptor()

# create a new archive
pe.create_archive(
    head_length=10, tail_length=10, password='123'
)
# adding files to it one by one, or all together in a list
pe.add_file('data/binary')
pe.add_file('data/img.jpg')
pe.add_file('data/text.txt')
pe.add_file_list([
    'data/binary2',
    'data/img2.jpg',
    'data/text2.txt'
])
# return a list of files added to archive
print(pe.list_files())
# save and clear current archive
output = pe.save_clear()

# "output" is a tuple with 3 parts
# tuple( head, middle, tail )
# the length of head and tail are defined in function create_archive()
print(type(output))
print(len(output))
# print the length of each part of output
print(list(map(len, list(output))))

# write all of them to out.7z
with open('out.7z', 'wb') as file:
    head,middle,tail = output
    file.write(head+middle+tail)

# you can save each part of the archive to different places
# so the archive become much harder to decrypt


# you can also chain these functions together

output = pe.create_archive(
    head_length=10, tail_length=10, password='123'
).add_file(
    'data/binary'
).add_file(
    'data/img.jpg'
).add_file(
    'data/text.txt'
).add_file_list([
    'data/binary2',
    'data/img2.jpg',
    'data/text2.txt'
]).save_clear()

```

