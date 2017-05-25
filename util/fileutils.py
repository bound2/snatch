import wget


def download_file(url, destination_folder):
    file_name = wget.download(url, out=destination_folder)
    return file_name

def delete_file(destination_folder, file_name):
    return