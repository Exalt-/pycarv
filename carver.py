#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re, os, io, hashlib
from PIL import Image, ImageFile

if __name__ == "__main__":

    #
    # list of all restults
    #
    results = []

    #
    # read file contents
    #
    contents = open("testimg.dd", "rb").read()

    #
    # signature data structure
    #
    signatures  = [ { "type":   "JPG", 
                      "header": "\xff\xd8\xff\xe0\x00\x10", 
                      "footer": "\xff\xd9", 
                      "indexes":{"headers":[], "footers":[]}},

                    { "type":   "JPG", 
                      "header": "\xff\xd8\xff\xe1", 
                      "footer": "\xff\xd9", 
                      "indexes":{"headers":[], "footers":[]}}]

    #
    # iterate over file signatures
    #
    for signature in signatures:

        #
        # find headers
        #
        signature["indexes"]["headers"] = [m.start() for m in re.finditer(signature["header"], contents)]

        #
        # find footers
        #
        signature["indexes"]["footers"] = [m.end() for m in re.finditer(signature["footer"], contents)]

        #
        # iterate over all signature index headers
        #
        for header in signature["indexes"]["headers"]:

            #
            # iterate over all signature index footers
            #
            for footer in signature["indexes"]["footers"]:
                    
                #
                # check if the footer is behind the header
                #
                if footer > header:

                    #
                    # data which will be used to reconstruct image file
                    #
                    artefact = contents[header:footer]

                    #
                    # create the artefact hash
                    #
                    art_hash = hashlib.sha224(artefact).hexdigest()

                    #
                    # generate filename
                    #
                    filename = art_hash + "." + signature["type"]

                    #
                    # check if file not already exists:
                    #
                    if not os.path.isfile("images/" + filename):

                        #
                        # saving the artefact as a reconstructed file
                        #
                        try:
                            stream   = io.BytesIO(artefact)     # turn artefact into a byte buffer
                            image    = Image.open(stream)       # open the bytebuffer as image
                            ImageFile.LOAD_TRUNCATED_IMAGES = True  # enable the saving of truncated images
                            image.save("images/" + filename)    # save image

                            #
                            # append the success to the results
                            #
                            results.append("succes " + filename)

                        except Exception as error:
                            #
                            # append the excepion to the results
                            #
                            results.append("error " + str(error))
                    else:
                        print "file exitsts"


    for result in results:
        if result.startswith("succes"):
            print result
        else:
            #
            # only for debugging
            #
            print result
