import os
import dxf2xml

dxf_folder_path = r"C:\Users\Morpheus\Desktop\Basic_training_models\outputs"
xml_folder_path1 = r"C:\Users\Morpheus\Desktop\AutoDimensions1.1\baseddata\training\With dimensions"
xml_folder_path2 = r"C:\Users\Morpheus\Desktop\AutoDimensions1.1\baseddata\training\Without dimensions"

# Check if the folder exists
if os.path.exists(dxf_folder_path) and os.path.isdir(dxf_folder_path):
    # Iterate through all the files in the folder
    for dxffilename in os.listdir(dxf_folder_path):
        # Check if the file is a DXF file
        if not dxffilename.endswith('.dxf'):
            continue
        dxffile_path = os.path.join(dxf_folder_path, dxffilename)
        xmlfile_path1 = os.path.join(xml_folder_path1, os.path.splitext(dxffilename)[0] + '.xml')
        xmlfile_path2 = os.path.join(xml_folder_path2, os.path.splitext(dxffilename)[0] + '.xml')
        if os.path.isfile(dxffile_path):
            dxf2xml.main(dxffile_path, xmlfile_path1, True)
            dxf2xml.main(dxffile_path, xmlfile_path2, False)