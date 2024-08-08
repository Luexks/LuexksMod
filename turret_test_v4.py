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
    
    return [(x1, y1), (x2, y2), (x3, y3)], base_length, height

def calculate_centroid(vertices):
    """Calculate the centroid of the triangle."""
    centroid_x = sum(x for x, y in vertices) / 3
    centroid_y = sum(y for x, y in vertices) / 3
    return (centroid_x, centroid_y)

def calculate_radius(vertices, centroid):
    """Calculate the radius as the square root of the average distance from the centroid to the vertices."""
    distances = [math.sqrt((x - centroid[0])**2 + (y - centroid[1])**2) for x, y in vertices]
    average_distance = sum(distances) / len(distances)
    return average_distance / 2

def update_plot(angle_deg, leg_length):
    """Update the plot based on the given angle and leg length."""
    vertices, base_length, height = calculate_vertices(angle_deg, leg_length)
    centroid = calculate_centroid(vertices)
    radius = calculate_radius(vertices, centroid)
    
    canvas.delete("all")  # Clear the canvas
    
    # Centering the triangle
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    center_x = canvas_width / 2
    center_y = canvas_height / 2
    
    # Adjust coordinates to center the triangle
    scaled_vertices = [(x + center_x, -y + center_y) for x, y in vertices]
    scaled_centroid = (centroid[0] + center_x, -centroid[1] + center_y)
    scaled_radius = radius
    
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
    
    angle_label.config(text=f"Angle: {angle_deg:.1f}°\nLeg Length: {leg_length}")

def on_scroll(event):
    """Handle scroll events to update the triangle angle or size."""
    global angle, leg_length, alt_pressed
    if alt_pressed:
        # Adjust leg length when Alt is pressed
        if event.delta > 0:  # Scroll up
            leg_length += 5
        else:  # Scroll down
            leg_length = max(10, leg_length - 5)  # Prevent leg length from going below 10
    else:
        # Adjust angle normally
        if event.delta > 0:  # Scroll up
            angle += 1
        else:  # Scroll down
            angle -= 1
        angle = max(10, min(90, angle))  # Keep angle between 10 and 90 degrees

    update_plot(angle, leg_length)

def on_key_press(event):
    """Handle key press events."""
    global alt_pressed
    if event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
        alt_pressed = True

def on_key_release(event):
    """Handle key release events."""
    global alt_pressed
    if event.keysym == 'Alt_L' or event.keysym == 'Alt_R':
        alt_pressed = False

# Initial angle and leg length
angle = 60
leg_length = 150
alt_pressed = False

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
canvas.pack(fill=tk.BOTH, expand=True)

# Create a label for displaying the angle
angle_label = tk.Label(root, text=f"Angle: {angle:.1f}°\nLeg Length: {leg_length}")
angle_label.pack()

# Bind the scroll event to the on_scroll function
root.bind("<MouseWheel>", on_scroll)
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Initial plot
update_plot(angle, leg_length)

# Start the Tkinter event loop
root.mainloop()
