import re

# Assume 'mtl_content' is the content of the MTL file
mtl_content = """
newmtl mtl1
Ka 0 0 0
Kd 0.5137254901960784 0.7098039215686275 1
Ks 0 0 0
Ns 1
Tr 1
illum 3
"""

# Initialize variables
material_name = ambient_color = diffuse_color = specular_color = None
specular_exponent = transparency = illumination_model = None

# Define regular expression patterns
pattern_material_name = re.compile(r'\s*newmtl\s+(\S+)')
pattern_color = re.compile(r'\s*([Kk][AaDdSs])\s+([0-9.]+)\s+([0-9.]+)\s+([0-9.]+)')
pattern_specular_exponent = re.compile(r'\s*Ns\s+([0-9.]+)')
pattern_transparency = re.compile(r'\s*Tr\s+([0-9.]+)')
pattern_illumination_model = re.compile(r'\s*illum\s+(\d+)')

# Split the content into lines and process each line
for line in mtl_content.splitlines():
    # Match material name
    match_material_name = pattern_material_name.match(line)
    if match_material_name:
        material_name = match_material_name.group(1)

    # Match color lines
    match_color = pattern_color.match(line)
    if match_color:
        colors = [float(match_color.group(i)) for i in range(2, 5)]
        if line.startswith('Ka'):
            ambient_color = colors
        elif line.startswith('Kd'):
            diffuse_color = colors
        elif line.startswith('Ks'):
            specular_color = colors

    # Match specular exponent
    match_specular_exponent = pattern_specular_exponent.match(line)
    if match_specular_exponent:
        specular_exponent = float(match_specular_exponent.group(1))

    # Match transparency
    match_transparency = pattern_transparency.match(line)
    if match_transparency:
        transparency = float(match_transparency.group(1))

    # Match illumination model
    match_illumination_model = pattern_illumination_model.match(line)
    if match_illumination_model:
        illumination_model = int(match_illumination_model.group(1))

# Print the extracted values
print("Material Name:", material_name)
print("Ambient Color:", ambient_color)
print("Diffuse Color:", diffuse_color)
print("Specular Color:", specular_color)
print("Specular Exponent:", specular_exponent)
print("Transparency:", transparency)
print("Illumination Model:", illumination_model)