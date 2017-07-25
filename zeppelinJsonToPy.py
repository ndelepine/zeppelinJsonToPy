#!/usr/bin/env

## AUTHOR: Lucas Tittmann & Nicolas Delepine
## LICENSE: Apache v 2.0
## PYTHON_VERSION : 2.7.11
##
## DESCRIPTION
##   Script to transform Apache Zeppelin [https://zeppelin.apache.org/]
##   JSON files into Python Scripts

import os
import sys
import json

def zeppelinJsonToPy(fileInput, fileOutput):

    """
    This function extracts the usefull content from a zeppelin JSON file and parse it into a Pyton script file.
    @Params
        fileInput = the filepath of the zeppelin JSON file
        fileOutput = the filepath of the .py file to write
    """

    with open(fileInput, "r") as f:
        dataStr = f.readline()
        data = json.loads(dataStr.decode("utf-8-sig"), encoding = "utf-8")

    out = ""
    for paragraph in data["paragraphs"]:
        paragraphText = paragraph["text"]

        try:
            # We write the paragraphe title
            paragraphTitle = paragraph["title"]
            out += "#" + "-" * (len(paragraphTitle) - 1) + "\n"
            out += "#" + paragraphTitle + "\n"
            out += "#" + "-" * (len(paragraphTitle) - 1) + "\n" * 2
        except:
            print("")

        # If it's a PySpark code, we append it to the output
        if paragraphText[0:len("%pyspark")] == "%pyspark":
            out += paragraphText[len("%pyspark"):]
            out += "\n"
            out += "\n" * 2
        # If it's a markdown file, we comment it and append it to the output
        if paragraphText[0:len("%md")] == "%md":
            lines = paragraphText.splitlines(True)
            for line in lines[1:]:
                # If its a main title that starts with '#', we surround it by '#'
                if line.startswith("#"):
                    out += "#" * len(line) + "\n"
                    out += line.replace("\n", "#") + "\n"
                    out += "#" * len(line) + "\n"
                # Else if it's a amin title that starts with <h1>, we replace the balises by '#' and surround it with '#'
                elif line.startswith("<h1>"):
                    out += "#" * (len(line) - 9) + "\n"
                    out += line.replace("<h1>", "#").replace("</h1>", "#")
                    out += "#" * (len(line) - 9) + "\n"
                # Else we add a "#"
                else:
                    if len(line) > 1:
                        out += "#" + line
            out += "\n" * 2

    with open(fileOutput, "w+") as f:
        f.write(out)
        f.truncate()
        f.close()

if __name__ == "__main__":
    #fileInput = sys.argv[1]
    fileInput="MY_FILE_PATH"
    fileBaseName = os.path.splitext(fileInput)[0]
    fileOutput = fileBaseName + ".py"
    print(fileInput)
    zeppelinJsonToPy(fileInput, fileOutput)
