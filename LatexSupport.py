def latexSymmetry(symmetry, color='black'):
    label_length = len(symmetry)
    last_character = label_length - 1
    if symmetry[:2].lower() == "pi":
        label = "\pi_{" + symmetry[2:].lower() + "}"
    elif symmetry[:2].lower() == "sg":
        label = "\sigma_{" + symmetry[2:].lower() + "}"
    elif symmetry[last_character:] == "'":
        label = symmetry[:1].upper()
        if label_length == 3:
            label = label + "_{" + symmetry[1] + "}"
        label = label + "^{\prime}"
    elif symmetry[last_character:] == "\"":
        label = symmetry[:1].upper()
        if label_length == 3:
            label = label + "_{" + symmetry[1] + "}"
        label = label + "^{\prime\prime}"
    elif symmetry[0] == "?":
        label = symmetry[1:].upper()
    else:
        label = (symmetry[:1].upper() + "_{" +
            symmetry[1:].lower() + "}")
    label = "\\(\\color{" + color + "}" + label + "\\)"
    return label
