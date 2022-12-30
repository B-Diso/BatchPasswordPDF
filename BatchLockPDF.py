import os
from multiprocessing import Pool
import PyPDF2




# Fungsi untuk mengunci file PDF
def lock_pdf(filename):
    print(filename)
    # Baca file PDF yang akan dikunci
    pdf_reader = PyPDF2.PdfReader(filename)
    pdf_writer = PyPDF2.PdfWriter()

    # Jika file PDF telah dikunci dengan password, abaikan file tersebut
    if pdf_reader.is_encrypted:
        print(f'**Sudah dikunci, skip {filename}')
        return

    # Loop melalui semua halaman dari file PDF
    for page in range(len(pdf_reader.pages)):
        # Tambahkan halaman ke dalam writer
        pdf_writer.add_page(pdf_reader.pages[page])

    # Tambahkan enkripsi ke file PDF yang telah ditulis
    password = 'MyAwesomePassword'
    pdf_writer.encrypt(password)

    # Tulis ke file PDF yang sama yang telah dikunci
    with open(filename, 'wb') as f:
        pdf_writer.write(f)


# Fungsi untuk melakukan scan folder secara rekursif
def scan_folder(folder):
    # Loop melalui semua file dan folder dalam folder yang sedang diolah
    for entry in os.scandir(folder):
        # Jika entry merupakan file dan berakhiran .PDF maka apend ke list pdfs
        if entry.is_file() and entry.name.endswith('.pdf'):
            pdfs.append(entry.path)
        # Jika entry merupakan folder, lakukan scan folder secara rekursif
        elif entry.is_dir():
            scan_folder(entry.path)


if __name__ == '__main__':
    pdfs = []
    scan_folder('.')
    pool = Pool()
    pool.map(lock_pdf, pdfs)
