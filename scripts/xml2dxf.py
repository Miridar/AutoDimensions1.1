import xml.etree.ElementTree as ET
import ezdxf

# Parse the XML file
tree = ET.parse(r"C:\Users\Morpheus\Desktop\Part1.xml")
root = tree.getroot()

# Create a new DXF file
dwg = ezdxf.new('R2010')

# Create a new dimension style
dim_style = dwg.styles.new('MyDimStyle')

# Set the DIMSCALE value to 0.5
dim_style.set_dimension_style(DIMSCALE=0.5)
dim_style.set_var('DIMASZ', 2)
dim_style.set_var('DIMEXO', 1)

# Access the modelspace of the DXF file
msp = dwg.modelspace()

# Iterate through the 'line' elements in the XML file
for line in root.findall('./lines/line'):
    # Get the start and end points of the line
    start = tuple(map(float, line.find('start').text[1:-1].split(',')))
    end = tuple(map(float, line.find('end').text[1:-1].split(',')))

    # Create a new LINE entity in the DXF file
    msp.add_line(start, end)

# Iterate through the 'dimension' elements in the XML file
for dimension in root.findall('./dimensions/dimension'):
    # Get the type, measurement, and definition points of the dimension
    dim_type = dimension.find('type').text
    measurment = dimension.find('measurment').text
    defpoint1_x, defpoint1_y, defpoint1_z = map(float, dimension.find('definitionPoint1').text[1:-1].split(','))
    defpoint1 = ezdxf.math.Vec2(defpoint1_x, defpoint1_y)
    defpoint2_x, defpoint2_y, defpoint2_z = map(float, dimension.find('definitionPoint2').text[1:-1].split(','))
    defpoint2 = ezdxf.math.Vec2(defpoint2_x, defpoint2_y)
    defpoint3_x, defpoint3_y, defpoint3_z = map(float, dimension.find('definitionPoint3').text[1:-1].split(','))
    defpoint3 = ezdxf.math.Vec2(defpoint3_x, defpoint3_y)
    angle = float(dimension.find('angle').text)
    leader_length = dimension.find('leaderLength').text

    # Create a new DIMENSION entity in the DXF file    
    if dim_type == "Linear and Rotated Dimension":
        msp.add_aligned_dim(defpoint2, defpoint3, 3.0)
    else:
        print(f"{dim_type} is not a supported dimension type.")
            
# Save the DXF file
dwg.saveas(r"C:\Users\Morpheus\Desktop\Part1_recreated.dxf")

# Print a message to the console
print("Code finished")
