import os
import shutil
import hashlib
from sys import platform

import gensim


def prepend_line(infile, outfile, line):
    with open(infile, 'r') as old:
        with open(outfile, 'w') as new:
            new.write(str(line) + "\n")
            shutil.copyfileobj(old, new)

def prepend_slow(infile, outfile, line):
    with open(infile, 'r') as fin:
        with open(outfile, 'w') as fout:
            fout.write(line + "\n")
            for line in fin:
                fout.write(line)


def checksum(filename):
    BLOCKSIZE = 65536
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
        buf = afile.read(BLOCKSIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(BLOCKSIZE)
    return hasher.hexdigest()


# Pre-computed glove files values.
pretrain_num_lines = {"glove.840B.300d.txt": 2196017, "glove.42B.300d.txt": 1917494}

pretrain_checksum = {
    "glove.6B.300d.txt": "b78f53fb56ec1ce9edc367d2e6186ba4",
    "glove.twitter.27B.50d.txt": "6e8369db39aa3ea5f7cf06c1f3745b06",
    "glove.42B.300d.txt": "01fcdb413b93691a7a26180525a12d6e",
    "glove.6B.50d.txt": "0fac3659c38a4c0e9432fe603de60b12",
    "glove.6B.100d.txt": "dd7f3ad906768166883176d69cc028de",
    "glove.twitter.27B.25d.txt": "f38598c6654cba5e6d0cef9bb833bdb1",
    "glove.6B.200d.txt": "49fa83e4a287c42c6921f296a458eb80",
    "glove.840B.300d.txt": "eec7d467bccfa914726b51aac484d43a",
    "glove.twitter.27B.100d.txt": "ccbdddec6b9610196dd2e187635fee63",
    "glove.twitter.27B.200d.txt": "e44cdc3e10806b5137055eeb08850569",
}


def check_num_lines_in_glove(filename, check_checksum=False):
    if check_checksum:
        assert checksum(filename) == pretrain_checksum[filename]
    if filename.startswith('glove.6B.'):
        return 400000
    elif filename.startswith('glove.twitter.27B.'):
        return 1193514
    else:
        return pretrain_num_lines[filename]


def load_glove_word2vec(filename):
    # Input: GloVe Model File
    # More models can be downloaded from http://nlp.stanford.edu/projects/glove/
    # print(filename[filename.rfind('/')+1:])

    glove_file = filename[filename.rfind('/')+1:]
    _, _,tokens, dimensions, _ = glove_file.split('.')
    num_lines = check_num_lines_in_glove(glove_file)
    dims = int(dimensions[:-1])

    # Output: Gensim Model text format.
    gensim_file = '/home/TCDteam12/glove/glove_model.txt'
    gensim_first_line = "{} {}".format(num_lines, dims)

    # Prepends the line.
    if platform == "linux" or platform == "linux2":
        prepend_line(filename, gensim_file, gensim_first_line)
    else:
        prepend_slow(filename, gensim_file, gensim_first_line)

    # Demo: Loads the newly created glove_model.txt into gensim API.
    model = gensim.models.KeyedVectors.load_word2vec_format(gensim_file, binary=False)  # GloVe Model

    return model

