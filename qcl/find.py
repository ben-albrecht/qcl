""" Submodule for finding stuff """

from __future__ import print_function

from os import path
from os import listdir


def tag(referencefile):
    """ Find tag file associated with the file provided

    :referencefile: Any file within a species directory
    :returns: absolute path to tag file
    """
    dirpath = path.abspath(referencefile)

    if path.isdir(dirpath):
        dircontents = listdir(dirpath)
    else:
        dirpath = path.split(dirpath)[0]
        dircontents = listdir(dirpath)

    while not 'tag' in dircontents:
        dirpath = path.split(dirpath)[0]
        dircontents = listdir(dirpath)
        if len(dircontents) == 0 or path.split(dirpath)[1] == 'chemistry':
            print("tag file not found")
            return None

    return path.join(dirpath, 'tag')



def fromtag(tofind, tag):
    """ Find a specific type of file, given a path to a tag file

    What to expect in a species directory, foo, with a tag file:

    (in order of generation)

    foo/
    foo/tag
    foo/foo.xyz
    foo/conformers
    foo/conformers/foo-conformers.xyz
    foo/conformers/[int].mp
    foo/conformers/[int].mp.out
    foo/conformers/[int].mp.arc
    foo/conformers/[int].qc.in
    foo/conformers/[int].qc.out
    foo/foo-opt.in
    foo/foo-opt.out
    foo/foo-freq.in
    foo/foo-freq.out
    foo/foo-pcm.in
    foo/foo-pcm.out
    foo/foo-emb.in
    foo/foo-emb.out
    foo/foo-emb.xml

    :tofind: file or directory to find
    :tag: path (absolute or relative) to tag file
    :returns: path to file/directory tofind, returns a list if multiple files
    """

    abstag = path.abspath(tag)
    speciespath = str(path.split(abstag)[0])
    species = str(path.split(speciespath)[1])
    conformers = str(path.join(speciespath, "conformers"))

    where = {
            "species"             : species,
            "speciespath"         : speciespath,
            "tag"                 : tag,
            "geometry"            : path.join(speciespath, species + ".xyz"),
            "conformers"          : conformers,
            "obconformer"        : path.join(conformers, species + "-conformers.xyz"),
            "conformermopacins"   : \
                [x for x in listdir(conformers) if x.endswith(".mp")],
            "conformermopacouts"  : \
                [x for x in listdir(conformers) if x.endswith(".mp.out")],
            "conformermopacarcs"  : \
                [x for x in listdir(conformers) if x.endswith(".mp.arc")],
            "conformerqchemins"  : \
                [x for x in listdir(conformers) if x.endswith(".qc.in")],
            "conformerqchemouts"  : \
                [x for x in listdir(conformers) if x.endswith(".qc.out")],
            "optin"               : path.join(speciespath, species + "-opt.in"),
            "optout"              : path.join(speciespath, species + "-opt.out"),
            "freqin"              : path.join(speciespath, species + "-freq.in"),
            "freqout"             : path.join(speciespath, species + "-freq.out"),
            "pcmin"               : path.join(speciespath, species + "-pcm.in"),
            "pcmout"              : path.join(speciespath, species + "-pcm.out"),
            "embin"               : path.join(speciespath, species + "-emb.in"),
            "embout"              : path.join(speciespath, species + "-emb.out"),
            "embxml"              : path.join(speciespath, species + "-emb.xml"),
            }
    if not tofind in where:
        print(tofind, " not a valid option for findfromtag")
        return None


    return where[tofind]
