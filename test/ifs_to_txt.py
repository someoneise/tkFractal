import os

# Specify the folder path
folder_path = 'ifs_files'

# List all files in the folder
files = os.listdir(folder_path)

flag = True

# Loop through each file
print(files)
for file_name in files:
    file_path = os.path.join(folder_path, file_name)

    # Check if the path is a file
    if os.path.isfile(file_path):
        with open(file_path, 'r', newline='') as file:
            with open(file_path[:-4]+'.txt', 'w') as newfile:
                file.__next__()
                while True:
                    line = file.readline().strip()
                    print(line)
                    if line == "}" or line == '':
                        break
                    newfile.write(line+'\n')
            newfile.close()
        file.close()
