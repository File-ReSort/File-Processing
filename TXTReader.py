def Read(fileLocation):
    with open(fileLocation) as f:
        text = f.read()

    return text