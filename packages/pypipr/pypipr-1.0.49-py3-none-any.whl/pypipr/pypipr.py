import os

def main():
    """
    Program utama
    """

    # Ambil semua file Python di dalam subfolder secara recursive
    files = [
        os.path.join(dirpath, filename)
        for dirpath, dirnames, filenames in os.walk(".")
        for filename in filenames
        if filename.endswith(".py") and filename != "__init__.py"
    ]

    # Urutkan daftar file berdasarkan nama file
    files.sort(key=lambda x: os.path.basename(x))

    # Print semua nama file dengan nomor urut
    for i, file in enumerate(files):
        filename = os.path.splitext(os.path.basename(file))[0]
        print(f"{i}. {filename}")

    # Minta input user berupa angka
    input_user = int(input("Pilih file Python yang ingin dijalankan (0-N): "))

    # Jalankan file Python yang dipilih
    os.system(f"python {files[input_user]}")

if __name__ == "__main__":
    main()

