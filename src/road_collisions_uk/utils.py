import os
import tarfile


def extract_tgz(filepath):
    tar = tarfile.open(filepath, 'r:gz')
    tar.extractall(path=os.path.dirname(filepath))
    tar.close()
