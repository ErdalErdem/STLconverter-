import numpy as np
from PIL import Image
from stl import mesh
from skimage import measure

# Load the image
image_path = "speda_logo.jpeg"
image = Image.open(image_path).convert("L")  # Convert to grayscale
image_array = np.array(image)

# Create a binary version of the image
binary_image = image_array < 128  # Assuming the logo is dark on light background

# Use marching squares to extract contours
contours = measure.find_contours(binary_image, 0.8)

# Create a 3D mesh by extruding the 2D contours
z_height = 5  # Height of the extrusion
vertices = []
faces = []
for contour in contours:
    for i, point in enumerate(contour[:-1]):
        x, y = point
        vertices.append([x, y, 0])
        vertices.append([x, y, z_height])
        if i > 0:
            faces.append([len(vertices) - 4, len(vertices) - 3, len(vertices) - 1])
            faces.append([len(vertices) - 4, len(vertices) - 1, len(vertices) - 2])

# Create a mesh object
logo_mesh = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
for i, face in enumerate(faces):
    for j in range(3):
        logo_mesh.vectors[i][j] = vertices[face[j]]

# Save the mesh to a file
output_path = "your_output_model.stl"
logo_mesh.save(output_path)

print(f"STL file saved as {output_path}")
