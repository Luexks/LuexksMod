import tkinter as tk
import math

def calculate_vertices(angle_deg, leg_length):
    """Calculate the vertices of an isosceles triangle given the vertex angle and leg length."""
    angle_rad = math.radians(angle_deg)
    
    # Calculate base length using the law of cosines
    base_length = 2 * leg_length * math.sin(angle_rad / 2)
    height = leg_length * math.cos(angle_rad / 2)
    
    x1, y1 = -base_length / 2, 0
    x2, y2 = base_length / 2, 0
    x3, y3 = 0, height
    
    return [(x1, y1), (x2, y2), (x3, y3)]

def distance_to_edge(centroid, vertex1, vertex2):
    """Calculate perpendicular distance from centroid to an edge defined by two vertices."""
    x0, y0 = centroid
    x1, y1 = vertex1
    x2, y2 = vertex2
    numerator = abs((y2 - y1) * x0 - (x2 - x1) * y0 + x2 * y1 - y2 * x1)
    denominator = math.sqrt((y2 - y1)**2 + (x2 - x1)**2)
    return numerator / denominator

def calculate_centroid(vertices):
    """Calculate the centroid of the triangle."""
    centroid_x = sum(x for x, y in vertices) / 3
    centroid_y = sum(y for x, y in vertices) / 3
    return (centroid_x, centroid_y)

def calculate_radius(vertices):
    """Calculate the radius of the circle centered at the triangle's centroid."""
    centroid = calculate_centroid(vertices)
    
    distances = [
        distance_to_edge(centroid, vertices[i], vertices[(i + 1) % 3])
        for i in range(3)
    ]
    
    average_distance = sum(distances) / len(distances)
    radius = average_distance
    
    return centroid, radius

def update_plot(angle_deg):
    """Update the plot based on the given angle."""
    leg_length = 150  # Fixed length for the two equal sides
    vertices = calculate_vertices(angle_deg, leg_length)
    centroid, radius = calculate_radius(vertices)
    
    canvas.delete("all")  # Clear the canvas
    
    # Scale and translate coordinates for better visualization
    scale = 1  # No scaling needed
    offset_x, offset_y = 200, 300  # Adjusted offset to move triangle lower
    
    scaled_vertices = [(x * scale + offset_x, -y * scale + offset_y) for x, y in vertices]
    scaled_centroid = (centroid[0] * scale + offset_x, -centroid[1] * scale + offset_y)
    scaled_radius = radius * scale
    
    # Draw the triangle
    canvas.create_polygon(scaled_vertices, outline='blue', fill='', width=2)
    
    # Draw the circle
    canvas.create_oval(
        scaled_centroid[0] - scaled_radius, scaled_centroid[1] - scaled_radius,
        scaled_centroid[0] + scaled_radius, scaled_centroid[1] + scaled_radius,
        outline='red', width=2
    )
    
    # Draw the centroid
    canvas.create_oval(
        scaled_centroid[0] - 3, scaled_centroid[1] - 3,
        scaled_centroid[0] + 3, scaled_centroid[1] + 3,
        fill='green'
    )
    
    angle_label.config(text=f"Angle: {angle_deg:.1f}°")

def on_scroll(event):
    """Handle scroll events to update the triangle angle."""
    global angle
    if event.delta > 0:  # Scroll up
        angle += 1
    else:  # Scroll down
        angle -= 1
    angle = max(10, min(90, angle))  # Keep angle between 10 and 90 degrees
    update_plot(angle)

# Initial angle
angle = 60

# Create the main window
root = tk.Tk()
root.title("Interactive Triangle and Circle")

# Set window transparency (Windows only)
root.attributes('-alpha', 0.7)  # Set transparency level (0.0 to 1.0, where 0.0 is fully transparent)

# Set window always on top
root.attributes('-topmost', True)

# Position the window at the top of the screen
root.geometry(f"400x400+{0}+{0}")  # Width x Height + X_offset + Y_offset

# Create a canvas for drawing
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# Create a label for displaying the angle
angle_label = tk.Label(root, text=f"Angle: {angle:.1f}°")
angle_label.pack()

# Bind the scroll event to the on_scroll function
root.bind("<MouseWheel>", on_scroll)

# Initial plot
update_plot(angle)

# Start the Tkinter event loop
root.mainloop()
