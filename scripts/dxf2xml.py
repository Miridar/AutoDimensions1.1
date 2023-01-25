import ezdxf
import xml.etree.ElementTree as ET
import xml.dom.minidom

def main(arg1, arg2, arg3):

    # Assign the arguments to variables
    dxfFilePath = arg1
    xmlFilePath = arg2
    dimensions = arg3

    # Open the DXF file
    dwg = ezdxf.readfile(dxfFilePath)

    # Access the modelspace of the DXF file
    msp = dwg.modelspace()

    # Create the root element for the XML tree
    root = ET.Element("root")

    # _________________________________________________________LINES_____________________________________________________________
    # Create a new lines element
    linesE = ET.SubElement(root, "lines")

    #set handle increment to 1
    handleIncrement = 1
    # Iterate through all the LINE entities in the modelspace
    for line in msp.query('LINE'):
        # Create a new line element
        lineE = ET.SubElement(linesE, "line")
        lineE.set("handle", "LINE_" + str(handleIncrement).zfill(4))
        round_point_coordinates(lineE, line.dxf.start, "start")
        round_point_coordinates(lineE, line.dxf.end, "end")
        handleIncrement = handleIncrement + 1
    
    # ___________________________________________________________CIRCLES_____________________________________________________________
    # Create a new circles element
    circlesE = ET.SubElement(root, "circles")

    #set handle increment to 1
    handleIncrement = 1
    # Iterate through all the CIRCLE entities in the modelspace
    for circle in msp.query('CIRCLE'):
        # Create a new circle element
        circleE = ET.SubElement(circlesE, "circle")
        circleE.set("handle", "CIRCLE_" + str(handleIncrement).zfill(4))
        round_point_coordinates(circleE, circle.dxf.center, "center")
        if isinstance(circle.dxf.radius, (int, float)):
            ET.SubElement(circleE, "radius").text = str(round(circle.dxf.radius, 2))
        else:
            ET.SubElement(circleE, "radius").text = str(dim.circle.dxf.radius)
        handleIncrement = handleIncrement + 1

    # ___________________________________________________________ARCS_____________________________________________________________
    # Create a new arcs element
    arcsE = ET.SubElement(root, "arcs")

    #set handle increment to 1
    handleIncrement = 1
    # Iterate through all the ARC entities in the modelspace
    for arc in msp.query('ARC'):
        # Create a new arc element
        arcE = ET.SubElement(arcsE, "arc")
        arcE.set("handle", "ARC_" + str(handleIncrement).zfill(4))
        round_point_coordinates(arcE, arc.dxf.center, "center")
        if isinstance(arc.dxf.radius, (int, float)):
            ET.SubElement(arcE, "radius").text = str(round(arc.dxf.radius, 2))
        else:
            ET.SubElement(arcE, "radius").text = arc.dxf.radius
        if isinstance(arc.dxf.start_angle, (int, float)):
            ET.SubElement(arcE, "startAngle").text = str(round(arc.dxf.start_angle, 2))
        else:
            ET.SubElement(arcE, "startAngle").text = arc.dxf.start_angle
        if isinstance(arc.dxf.end_angle, (int, float)):
            ET.SubElement(arcE, "endAngle").text = str(round(arc.dxf.end_angle, 2))
        else:
            ET.SubElement(arcE, "endAngle").text = arc.dxf.end_angle
        round_point_coordinates(arcE, arc.start_point, "startPoint")
        round_point_coordinates(arcE, arc.end_point, "endPoint")

        handleIncrement = handleIncrement + 1

    # _________________________________________________________DIMENSIONS_____________________________________________________________
    if dimensions:
        # Create a new dimensions element
        dimsE = ET.SubElement(root, "dimensions")

        #set handle increment to 1
        handleIncrement = 1
        # Iterate through all the DIMENSION entities in the modelspace
        for dim in msp.query('DIMENSION'):
            # Create a new dimension element
            dimE = ET.SubElement(dimsE, "dimension")
            dimE.set("handle", "DIMENSION_" + str(handleIncrement).zfill(4))
            ET.SubElement(dimE, "type").text = get_dimension_type(dim.dxf.dimtype)
            if isinstance(dim.get_measurement(), (int, float)):
                ET.SubElement(dimE, "measurment").text = str(round(dim.get_measurement(), 2))
            else:
                ET.SubElement(dimE, "measurment").text = str(dim.get_measurement())
            round_point_coordinates(dimE, dim.dxf.defpoint, "definitionPoint1")
            round_point_coordinates(dimE, dim.dxf.defpoint2, "definitionPoint2")
            round_point_coordinates(dimE, dim.dxf.defpoint3, "definitionPoint3")
            round_point_coordinates(dimE, dim.dxf.defpoint4, "definitionPoint4")
            round_point_coordinates(dimE, dim.dxf.defpoint5, "definitionPoint5")
            if isinstance(dim.dxf.angle, (int, float)):
                ET.SubElement(dimE, "angle").text = str(round(dim.dxf.angle, 2))
            else:
                ET.SubElement(dimE, "angle").text = str(dim.dxf.angle)
            if isinstance(dim.dxf.leader_length, (int, float)):
                ET.SubElement(dimE, "leaderLength").text = str(round(dim.dxf.leader_length, 2))
            else:
                ET.SubElement(dimE, "leaderLength").text = str(dim.dxf.leader_length)

    
    # ________________________________________________________________________________________________________________________

    # Write the XML tree to a file
    tree = ET.ElementTree(root)
    tree.write(xmlFilePath)

    # Format the XML file
    format_xml(xmlFilePath)

    # Print a message to the console
    print("Code finished")

# Function to format the XML file
def format_xml(file_name: str):
    # Open the XML file and parse it
    xml_file = open(file_name, "r")
    xml_str = xml_file.read()
    xml_file.close()

    # Use the parseString method to parse the XML string
    xml_dom = xml.dom.minidom.parseString(xml_str)

    # Use the toprettyxml method to format the XML
    pretty_xml_str = xml_dom.toprettyxml()

    # Write the formatted XML string to a file
    pretty_xml_file = open(file_name, "w")
    pretty_xml_file.write(pretty_xml_str)
    pretty_xml_file.close()

# Function to get the dimension type as a string
def get_dimension_type(dimtype: int) -> str:
    dimtype_map = {
        0: "Linear and Rotated Dimension",
        1: "Aligned Dimension",
        2: "Angular Dimension",
        3: "Diameter Dimension",
        4: "Radius Dimension",
        5: "Angular 3P Dimension",
        6: "Ordinate Dimension",
        8: "subclass ezdxf.entities.ArcDimension"
    }
    dimtype_str = dimtype_map.get(dimtype & ~(32 | 64 | 128), "Unknown")
    return dimtype_str

# Function to round the coordinates of a coordinate tuple and add it to the XML file
def round_point_coordinates(dimE, coordinates, name):
    coordinates = str(coordinates)
    if coordinates.startswith("(") and coordinates.endswith(")"):
        coordinates = coordinates[1:-1]
        coordinates = [round(float(x), 2) for x in coordinates.split(", ")]
        coordinates = f"({coordinates[0]}, {coordinates[1]}, {coordinates[2]})"
        ET.SubElement(dimE, name).text = coordinates
    else:
        ET.SubElement(dimE, name).text = coordinates

if __name__ == '__main__':
    main()