"""
This method reads a generated list of cells vs. names as assigned by OpenWorm backers

This information will eventually be moved to owmeta/elsewhere...
"""

import os

currentfile_dir = os.path.dirname(os.path.abspath(__file__))


def get_adopted_cell_names(root=os.path.join(currentfile_dir, "data")):
    with open(os.path.join(root, "adopters.txt")) as file:
        ads = {}
        for line in file:
            cell = line.split(":")[0].strip()
            name = line.split(":")[1].strip()
            ads[cell] = name

    return ads


if __name__ == "__main__":
    ads = get_adopted_cell_names()

    file = open("cells.md", "w")

    info = ""

    info += "Cells which have been adopted in the OpenWorm project\n"
    info += "=====================================================\n\n"
    info += "The majority of these cells were sponsored by contributors during the Kickstarter campaign in 2014.\n\n"
    info += '<p align="center">\n'
    info += '  <img src="https://raw.githubusercontent.com/openworm/c302/experimental/images/SomeCells.png" alt="Some cells"/>\n'
    info += "</p>\n\n"

    url = (
        "https://github.com/openworm/c302/blob/master/examples/c302_C_Full.net.nml#L%i"
    )

    osb_3d_url = "https://v1.opensourcebrain.org/projects/c302/models?explorer=https%253A%252F%252Fraw.githubusercontent.com%252Fopenworm%252Fc302%252Fmaster%252Fc302%252FNeuroML2%252F"

    for cell in sorted(ads.keys()):
        name = ads[cell]
        info += cell + "\n"
        info += "----------\n\n"
        info += "Adopted name: **" + name + "**\n\n\n"
        i = 0
        search_file = open(
            os.path.normpath(
                os.path.join(currentfile_dir, "..", "examples", "c302_C_Full.net.nml")
            ),
            "r",
        )
        for line in search_file:
            i += 1
            if 'tag="OpenWormBackerAssignedName" value="%s"' % name in line:
                info += "Added to c302 network files [here](%s).\n\n" % (url % i)

        info += "This cell can be viewed in 3D [here](%s) (requires WebGL).\n\n" % (
            osb_3d_url + cell + ".cell.nml"
        )

    print(info)
    file.write(info)
    file.close()
