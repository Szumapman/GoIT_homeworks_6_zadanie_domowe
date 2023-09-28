import sys
import os
import shutil

# files = os.scandir("C:/Projects/GoIT_homeworks/6/Bałagan")
# for file in files:
#     if file.is_file():
#         print(file.path)
# shutil.move("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.replace("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.rename("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/Nowy/lis.pdf")
# os.renames("C:/Projects/GoIT_homeworks/6/Bałagan/lis.pdf", "C:/Projects/GoIT_homeworks/6/Bałagan/New/lis.pdf")

# os.makedirs("Bałagan/Test")
# os.rmdir("C:/Projects/GoIT_homeworks/6/Bałagan/Test")

def get_path():
    exit_help = f"Stars program with command like: {sys.argv[0]} /user/folder_to_sort/ (path to folder you want to sort)."
    if len(sys.argv) < 2:
        sys.exit(f"Too few command-line arguments.\n{exit_help}")
    elif len(sys.argv) > 2:
        sys.exit(f"Too many command line arguments.\n{exit_help}")
    folder_path = sys.argv[1]
    if os.path.exists(os.path.dirname(folder_path)):
        return folder_path
    sys.exit(f"{folder_path} is not a proper folder path.\n{exit_help}")

def sort_folder(path):
    files = os.scandir(path)
    for file in files:
        if file.is_dir():
            print(f"folder: {file.name}")
        else:
           file_name, ext = os.path.splitext(file.name)
           file_name = normalize(file_name)
           dest_folder_name = ""
           match ext:
               case ".pdf" | ".txt":
                   dest_folder_name = "documents/"

           os.renames(f"{path}/{file.name}", f"{path}{dest_folder_name}{file_name}{ext}")

def normalize(name: str) -> str:
    # tworzę słownik polskich znaków, które będę zamieniał na odpowiedniki łacińskie
    map = {
        ord('ą'): 'a', ord('Ą'): 'A',
        ord('ć'): 'c', ord('Ć'): 'C',
        ord('ę'): 'e', ord('Ę'): 'E',
        ord('ł'): 'l', ord('Ł'): 'L',
        ord('ń'): 'n', ord('Ń'): 'N',
        ord('ó'): 'o', ord('Ó'): 'O',
        ord('ś'): 's', ord('Ś'): 'Ś',
        ord('ź'): 'z', ord('Ż'): 'Z',
        ord('ż'): 'z', ord('Ż'): 'Z',   
    }
    normalized_name = name.translate(map) # zmieniam polskie znaki na łacińskie odpowiedniki 
    
    # zmieniam inne niedozwolone w nazwie znaki na znak _
    for chr in normalized_name:
        if not (48 <= ord(chr) <= 57 or 65 <= ord(chr) <= 90 or 97 <= ord(chr) <= 122 or ord(chr) == 95):
            normalized_name = normalized_name.translate({ord(chr): '_'})
    return normalized_name
    

def main():
    sort_folder(get_path())

if __name__ == "__main__":
    main()



