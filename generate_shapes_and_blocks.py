import math

def combine_list_of_lists(list_of_lists: list) -> list:
    output = []
    for list in list_of_lists:
        output += list
    return output

VERTEX_ORIENTATION_MULTIPLIERS = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
SHAPE_ID_ROOT = "201923"
SHAPE_ID_SERIAL_LENGTH = 4
TOTAL_SCALE = 10

SHROUD_TURRET_RADIUS_OFFSET_MULTIPLIER = 0.5 # big name

SHROUD_CIRLCE_SIDE_COUNT = 32

SHROUD_SCALE_X_OFFSET = 2.5
SHROUD_OUTLINE_MULTIPLIER = 0.5
SHROUD_BACKGROUND_MULTIPLIER = 8

SHROUD_BACKGROUND_COLOR = "FFFFFF"
SHROUD_BACKGROUND_X_SCALE_COUNT = 16
SHROUD_BACKGROUND_X_SCALE_FACTOR = TOTAL_SCALE * 16
SHROUD_BACKGROUND_Y_SCALE_COUNT = 16
SHROUD_BACKGROUND_Y_SCALE_FACTOR = TOTAL_SCALE * 16

SHROUD_Z_OFFSET_FILL = "-0.02"
# SHROUD_Z_OFFSET_OUTLINE = "-0.06"
SHROUD_Z_OFFSET_OUTLINE = "-0.01"
SHROUD_Z_OFFSET_BACKGROUND = "-1"
if 0 == 1:
    SHROUD_OUTLINE_CIRCLE_DIAMETER = 0
else:
    SHROUD_OUTLINE_CIRCLE_DIAMETER = TOTAL_SCALE / 2
SHROUD_OUTLINE_THICKNESS = SHROUD_OUTLINE_CIRCLE_DIAMETER / 2

BLOCK_ID_BASE = 17000
BLOCK_SORT_BASE = 100

SQUARE_SCALE_COUNT = 3
SQUARE_SCALE_FACTOR = TOTAL_SCALE / 2

TRIANGLE_X_SCALE_COUNT = 3 * 2
TRIANGLE_X_SCALE_FACTOR = TOTAL_SCALE / 2
TRIANGLE_Y_SCALE_COUNT = 3 * 2
TRIANGLE_Y_SCALE_FACTOR = TOTAL_SCALE / 2

RECTANGLE_SCALE_FUNCTIONS = combine_list_of_lists([
    [
        (lambda x: x * 0.5, lambda y: y * 0.5),
        (lambda x: x, lambda y: y * 0.5)
    ],
    combine_list_of_lists([(lambda x, scale=scale: x * scale, lambda y, scale=scale: scale * (y - y / math.sqrt(2))) if i == 0 else (lambda x, scale=scale: x * scale, lambda y, scale=scale: scale * (y / math.sqrt(2))) for i in range(0, 2, 1)] for scale in range(1, 7, 1))
])

ADAPTER_SCALE_COUNT = 5

ISOTRI_MIN_ANGLE = 10 # Anything below roughly 10 can cause corruption through the mirroring test and is thus not advisable.
ISOTRI_MAX_ANGLE = 90
ISOTRI_SCALE_INTERVAL_ANGLE = 1
ISOTRI_SCALE_COUNT = 3

if (ISOTRI_MAX_ANGLE - ISOTRI_MIN_ANGLE) % ISOTRI_SCALE_INTERVAL_ANGLE != 0:
    print("Isotri fuckup, pls revise.")

block_id = BLOCK_ID_BASE

def new_block_id() -> int:
    global block_id
    block_id += 1
    return block_id - 1

block_sort = BLOCK_SORT_BASE

def new_block_sort() -> int:
    global block_sort
    block_sort += 1
    return block_sort - 1

def shape_id(serial: int) -> str:
    shape_id = SHAPE_ID_ROOT
    for i in range(SHAPE_ID_SERIAL_LENGTH - len(str(serial))):
        shape_id += "0"
    shape_id += str(serial)

    return shape_id

def unison_shroud_colors(color_id: int) -> str:
    return f"tri_color_id={str(color_id)},tri_color1_id={str(color_id)},line_color_id={str(color_id)}"

def mirror_vertices(vertices: [(float, float)]) -> [(float, float)]:
    mirrored_vertices = vertices
    for vertex_index in range(len(vertices)):
        mirrored_vertices[vertex_index] = (vertices[vertex_index][0], vertices[vertex_index][1] * -1)
    mirrored_vertices.reverse()
    return mirrored_vertices


def write_scale_format(verts: list[(float, float)], ports: list[(int, str)]) -> None:
    global shapes
    shapes.write("\n\t\t\t{\n\t\t\t\tverts={")
    for vert in verts:
        shapes.write(f"{{{str(vert[0])},{str(vert[1])}}}")
    shapes.write("}\n\t\t\t\tports={")
    for port in ports:
        shapes.write(f"{{{str(port[0])},{port[1]}}}")
    shapes.write("}\n\t\t\t}")

class MininumPortToVertexDistanceParsedWhenUnneeded(Exception):
    def __init__(self) -> None:
        super().__init__("mininum_port_to_vertex_distance parsed when unneeded. If you were using Rust, then this wouldn't be an issue >:(")

class MininumPortToVertexDistanceNotParsedWhenNeeded(Exception):
    def __init__(self) -> None:
        super().__init__("mininum_port_to_vertex_distance is not parsed when needed. If you were using Rust, then this wouldn't be an issue >:(")

class InvalidPortRelativeToOptionValue(Exception):
    def __init__(self) -> None:
        super().__init__("Invalid port_relative_to_option value. It's sort of meant to be an enum, it should only ever be either 0, 1, or 2; if you were using Rust, then this wouldn't be an issue >:(")

def write_shroud_outline(vertices: list[(float, float)], offset: (float, float)) -> None:
    global blocks
    for vertex_index in range(len(vertices)):
        blocks.write(f"{{shape={shape_id(9000)},offset={{{str(vertices[vertex_index][0] + offset[0])},{str(vertices[vertex_index][1] + offset[1])},{SHROUD_Z_OFFSET_OUTLINE}}},size={{{SHROUD_OUTLINE_CIRCLE_DIAMETER},{SHROUD_OUTLINE_CIRCLE_DIAMETER}}},tri_color_id=2,tri_color1_id=2,line_color_id=2}}{{shape=SQUARE,offset={{{str(0.5 * (vertices[vertex_index][0] + vertices[(vertex_index + 1) % len(vertices)][0]) + offset[0])},{str(0.5 * (vertices[vertex_index][1] + vertices[(vertex_index + 1) % len(vertices)][1]) + offset[1])},{SHROUD_Z_OFFSET_OUTLINE}}},size={{{SHROUD_OUTLINE_THICKNESS},{0.5 * math.sqrt((vertices[vertex_index][0] - vertices[(vertex_index + 1) % len(vertices)][0]) ** 2 + (vertices[vertex_index][1] - vertices[(vertex_index + 1) % len(vertices)][1]) ** 2)}}},angle={str(-90 * (math.pi / 180) + math.atan2(vertices[vertex_index][1] - vertices[(vertex_index + 1) % len(vertices)][1], vertices[vertex_index][0] - vertices[(vertex_index + 1) % len(vertices)][0]))},tri_color_id=2,tri_color1_id=2,line_color_id=2}}")

# port_relative_to_option describes whether the ports should be positioned relative to the middle of the shape (0), or relative to vertex_1 (1), or relative to vertex_2 (2)
# When port_relative_to_option != 0, mininum_port_to_vertex_distance is parsed as a float.
def generate_spaced_ports(vertex_1: tuple[float, float], vertex_2: tuple[float, float], port_spacing: float, side_index: int, port_relative_to_option: int, mininum_port_to_vertex_distance: float = None) -> list[(int, float)]:
    side_length = math.sqrt((vertex_1[0] - vertex_2[0]) ** 2 + (vertex_1[1] - vertex_2[1]) ** 2)
    port_count = math.floor(side_length / port_spacing)
    
    if port_count <= 1 and side_length <= port_spacing:
        return [(side_index, 0.5)]

    # if port_count % 2 == 0: # I guess it works without the code I thought it would need :P
        # return [(side_index, (0.5 - (port_spacing * (port_count / 2 - 0.5)) / side_length + port_index * port_spacing / side_length)) for port_index in range(int(port_count))]
    
    if port_relative_to_option == 0:
        if mininum_port_to_vertex_distance is not None:
            raise MininumPortToVertexDistanceParsedWhenUnneeded
        return [(side_index, (0.5 - (port_spacing * (port_count / 2 - 0.5)) / side_length + port_index * port_spacing / side_length)) for port_index in range(int(port_count))]
    else:
        if mininum_port_to_vertex_distance is None:
            raise MininumPortToVertexDistanceNotParsedWhenNeeded

        elif port_relative_to_option == 1:
            ports = [(side_index, mininum_port_to_vertex_distance / side_length + port_index * (port_spacing / side_length)) for port_index in range(int(port_count))]
            # print(side_length % port_spacing)
            if side_length % port_spacing > 0:
                ports.append((side_index, 1.0 - ((side_length % port_spacing) / side_length) / 2.0))
            return ports

        elif port_relative_to_option == 2:
            ports = [(side_index, 1.0 - (mininum_port_to_vertex_distance / side_length + port_index * (port_spacing / side_length))) for port_index in range(int(port_count))]
            if side_length % port_spacing > 0:
                ports.append((side_index, 0.0 + ((side_length % port_spacing) / side_length) / 2.0))
            return ports

        else:
            raise InvalidPortRelativeToOptionValue

with open("shapes.lua", "w", encoding="utf-8") as shapes, open("blocks.lua", "w", encoding="utf-8") as blocks:
    ### HULL SHAPES ###
    shapes.write("{")

    # Squares
    vertices_square = []
    shapes.write(f"\n\t{{{shape_id(0)}\n\t\t{{")
    for scale in range(1, SQUARE_SCALE_COUNT + 1):
        new_vertices = [(scale * SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][0], scale * SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][1]) for vertex_orientation in range(4)]
        vertices_square.append(new_vertices)
        write_scale_format(new_vertices, combine_list_of_lists([[(side, f"{str(port * 2 + 1)}/{str((scale) * 2)}") for port in range(scale)] for side in range(4)]))
    shapes.write("\n\t\t}\n\t}")

    # Right Triangles
    vertices_right_triangle = []
    triangle_count = 0
    triangle_block_data = []
    shapes.write(f"\n\t{{{shape_id(1)}\n\t\t{{")
    for scale_y in range(1, TRIANGLE_Y_SCALE_COUNT + 1):
        for scale_x in range(scale_y, TRIANGLE_X_SCALE_COUNT + 1):
            new_vertices = [(0, 0), (0, scale_y * TRIANGLE_Y_SCALE_FACTOR), (scale_x * TRIANGLE_X_SCALE_FACTOR, 0)]
            vertices_right_triangle.append(new_vertices)
            triangle_block_data.append((new_vertices[1][1], new_vertices[2][0]))
            write_scale_format(new_vertices, combine_list_of_lists([generate_spaced_ports(new_vertices[0], new_vertices[1], TOTAL_SCALE, 0, 1, TOTAL_SCALE / 2), generate_spaced_ports(new_vertices[1], new_vertices[2], TOTAL_SCALE, 1, 0), generate_spaced_ports(new_vertices[2], new_vertices[0], TOTAL_SCALE, 2, 2, TOTAL_SCALE / 2)]))
            triangle_count += 1
            # if new_vertices[1][1] >= new_vertices[2][0]:
                # break
    shapes.write("\n\t\t}\n\t}\n\t")

    shapes.write(f"\n\t{{{shape_id(2)}{{}}mirror_of={shape_id(1)}}}")

    # Rectangles
    vertices_rectangle = []
    shapes.write(f"\n\t{{{shape_id(3)}\n\t\t{{")
    for rectangle_scale_function in RECTANGLE_SCALE_FUNCTIONS:
        new_vertices = [(rectangle_scale_function[0](SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][0]), rectangle_scale_function[1](SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][1])) for vertex_orientation in range(4)]
        vertices_rectangle.append(new_vertices)
        write_scale_format(new_vertices, combine_list_of_lists([generate_spaced_ports(new_vertices[side], new_vertices[(side + 1) % len(new_vertices)], TOTAL_SCALE, side, 0) for side in range(0, 4, 1)]))
    shapes.write("\n\t\t}\n\t}")

    # Adapters
    shapes.write(f"\n\t{{{shape_id(4)}\n\t\t{{")
    write_scale_format([(SQUARE_SCALE_FACTOR / -2, SQUARE_SCALE_FACTOR * -1), (SQUARE_SCALE_FACTOR / -2, SQUARE_SCALE_FACTOR), (SQUARE_SCALE_FACTOR / 2, 0)], [(0, 0.5), (1, 0.5), (2, 0.5)])
    for scale in range(1, ADAPTER_SCALE_COUNT + 1 - 1):
        new_vertices = [((SQUARE_SCALE_FACTOR / 2) * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][0], (scale * SQUARE_SCALE_FACTOR + SQUARE_SCALE_FACTOR / 2 - SQUARE_SCALE_FACTOR * (0.5 if vertex_orientation in [0, 2] else -0.5) * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][1]) * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][1]) for vertex_orientation in range(4)]
        write_scale_format(new_vertices, combine_list_of_lists([generate_spaced_ports(new_vertices[side], new_vertices[(side + 1) % len(new_vertices)], TOTAL_SCALE, side, 0) for side in range(0, 4, 1)]))
    shapes.write("\n\t\t}\n\t}")

    # Isotris
    shapes.write(f"\n\t{{{shape_id(5)}\n\t\t{{")
    for angle in range(ISOTRI_MIN_ANGLE, ISOTRI_MAX_ANGLE, ISOTRI_SCALE_INTERVAL_ANGLE):
        for scale in range(1, ISOTRI_SCALE_COUNT + 1):
            new_vertices = [(-math.cos(math.radians(angle / 2)) * scale * TOTAL_SCALE, -math.sin(math.radians(angle / 2)) * scale * TOTAL_SCALE), (-math.cos(math.radians(angle / 2)) * scale * TOTAL_SCALE, math.sin(math.radians(angle / 2)) * scale * TOTAL_SCALE), (0, 0)]
            write_scale_format(new_vertices, combine_list_of_lists([generate_spaced_ports(new_vertices[0], new_vertices[(1)], TOTAL_SCALE, 0, 0)] + [[(side, f"{str(port * 2 + 1)}/{str((scale) * 2)}") for port in range(scale)] for side in range(1, 3)]))
    shapes.write("\n\t\t}\n\t}")


    ### SHROUD SHAPES ###

    shapes.write(f"\n\t{{{shape_id(9000)}\n\t\t{{")

    # Shroud Circle
    radius = TOTAL_SCALE / (2 * math.sin(math.pi / SHROUD_CIRLCE_SIDE_COUNT))
    new_vertices = []
    angle_between_vertices = 2 * math.pi / SHROUD_CIRLCE_SIDE_COUNT

    for side_index in range(SHROUD_CIRLCE_SIDE_COUNT):
        angle_from_origin = side_index * angle_between_vertices
        new_vertices.append((radius * math.cos(angle_from_origin), radius * math.sin(angle_from_origin)))
    
    write_scale_format(new_vertices, [(0, 0)])

    shapes.write("\n\t\t}\n\t}")

    # Shroud Background
    shroud_background_block_data = []
    shapes.write(f"\n\t{{{shape_id(9001)}\n\t\t{{")
    for scale_y in range(1, SHROUD_BACKGROUND_Y_SCALE_COUNT + 1):
        for scale_x in range(scale_y, SHROUD_BACKGROUND_X_SCALE_COUNT + 1):
            write_scale_format(vertices_square[0], combine_list_of_lists([[(side, f"{str(port * 2 + 1)}/{str((1) * 2)}") for port in range(1)] for side in range(4)]))
    shapes.write("\n\t\t}\n\t}\n\t")

    shapes.write("\n}")

    ### BLOCKS ###

    blocks.write(f"\n{{\n\t{{{str(new_block_id())}\n")
    with open("start_of_blocks.lua", "r") as start_of_blocks:
        blocks.write(start_of_blocks.read())
    blocks.write(f"\n\n\t\tsort={str(new_block_sort())}\n\t\tshape={shape_id(0)}\n\t\tscale=1\n\t")

    # Squares
    blocks.write(f"\t\n\t\tshroud={{")
    write_shroud_outline(vertices_square[0], (2.5, 0.0))
    blocks.write("}\n\t}")
    # blocks.write(f"\t\n\t\tshroud={{{{shape={shape_id(0)},offset={{{str(SHROUD_SCALE_X_OFFSET)},0.0,{SHROUD_Z_OFFSET_FILL}}},size={{{str(TOTAL_SCALE)},{str(TOTAL_SCALE)}}},{unison_shroud_colors(0)}}}{{shape={shape_id(0)},offset={{{str(SHROUD_SCALE_X_OFFSET)},0.0,{SHROUD_Z_OFFSET_OUTLINE}}},size={{{str(TOTAL_SCALE + TOTAL_SCALE * SHROUD_OUTLINE_MULTIPLIER)},{str(TOTAL_SCALE + TOTAL_SCALE * SHROUD_OUTLINE_MULTIPLIER)}}},{unison_shroud_colors(2)}}}{{shape={shape_id(0)},offset={{{str(SHROUD_SCALE_X_OFFSET)},0.0,{SHROUD_Z_OFFSET_BACKGROUND}}},size={{{str(TOTAL_SCALE + TOTAL_SCALE * SHROUD_BACKGROUND_MULTIPLIER)},{str(TOTAL_SCALE + TOTAL_SCALE * SHROUD_BACKGROUND_MULTIPLIER)}}},{unison_shroud_colors(1)}}}}}\n\t}}")
    for scale in range(SQUARE_SCALE_COUNT - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(BLOCK_ID_BASE)},durability=2.00001,scale={str(scale + 2)},shroud={{")
        write_shroud_outline(vertices_square[scale + 1], (2.5 * (scale + 2), 0.0))
        blocks.write("}}")

    # Right Triangles
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,shape={shape_id(1)},shroud={{")
    pwoomee = 5.0 * (1 / 3)
    # write_shroud_outline(vertices_right_triangle[0], (0.0, 0.0))
    write_shroud_outline(vertices_right_triangle[0], (0.59 - pwoomee, 0.0 - pwoomee))
    # write_shroud_outline(vertices_right_triangle[0], (math.cos(45) * (1 / 3), math.sin(45) * (1 / 3)))
    # write_shroud_outline(vertices_right_triangle[0], (-4 * math.sin(45) * (1 / 3), -6 * math.sin(45) * (1 / 3)))
    blocks.write("}}")
    scale = 0
    for scale_y in range(1, TRIANGLE_Y_SCALE_COUNT + 1):
        for scale_x in range(scale_y + (1 if scale_y == 1 else 0), TRIANGLE_X_SCALE_COUNT + 1):
            blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)},shroud={{}}}}")
            scale += 1

    # Mirrored Right Triangles
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,shape={shape_id(2)},shroud={{")
    # write_shroud_outline(mirror_vertices(vertices_right_triangle[0]), (0.0, 0.0))
    write_shroud_outline(mirror_vertices(vertices_right_triangle[0]), (0.59 - pwoomee, 0.0 + pwoomee))
    blocks.write("}}")
    for scale in range(triangle_count - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)}}}")

    # Rectangles
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,shape={shape_id(3)},shroud={{")
    write_shroud_outline(vertices_rectangle[0], (vertices_rectangle[0][1][1] * SHROUD_TURRET_RADIUS_OFFSET_MULTIPLIER, 0.0))
    blocks.write("}}")
    for scale in range(len(RECTANGLE_SCALE_FUNCTIONS) - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)},shroud={{")
        write_shroud_outline(vertices_rectangle[scale + 1], (vertices_rectangle[scale + 1][1][1] * SHROUD_TURRET_RADIUS_OFFSET_MULTIPLIER, 0.0))
        blocks.write("}}")

    # Adapter
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,shape={shape_id(4)}}}")
    for scale in range(ADAPTER_SCALE_COUNT - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)}}}")

    # Isotris
    new_extend_parent_id = new_block_id()
    for angle in range(ISOTRI_MIN_ANGLE, ISOTRI_MAX_ANGLE, ISOTRI_SCALE_INTERVAL_ANGLE):
        for scale in range(ISOTRI_SCALE_COUNT):
            if angle == ISOTRI_MIN_ANGLE and scale == 0:
                blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,shape={shape_id(5)},blurb=\"{f'{str(angle)}'}°\\nStructural definition\"}}")
            else:
                blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(((angle - ISOTRI_MIN_ANGLE) // ISOTRI_SCALE_INTERVAL_ANGLE) * ISOTRI_SCALE_COUNT + scale + 1)},blurb=\"{f'{str(angle)}'}°\\nStructural definition\"}}")

    # Shroud Background
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},sort={str(new_block_sort())},durability=2.00001,lineColor=0x{SHROUD_BACKGROUND_COLOR},shape={shape_id(9001)},name=\"Background Component\",blurb=\"Scaled for different sizes of aesthetic backgrounds\"}}")
    scale = 2
    for scale_y in range(1, SHROUD_BACKGROUND_Y_SCALE_COUNT):
        for scale_x in range(scale_y, SHROUD_BACKGROUND_X_SCALE_COUNT + 1):
            blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale)},blurb=\"{str(scale_x * SHROUD_BACKGROUND_X_SCALE_FACTOR)},{str(scale_y * SHROUD_BACKGROUND_Y_SCALE_FACTOR)}\\nScaled for different sizes of aesthetic backgrounds\",shroud={{{{shape={shape_id(0)},offset={{2.5,0.0,{SHROUD_Z_OFFSET_BACKGROUND}}},size={{{str(scale_x * SHROUD_BACKGROUND_X_SCALE_FACTOR)},{str(scale_y * SHROUD_BACKGROUND_Y_SCALE_FACTOR)}}},{unison_shroud_colors(2)}}}}}}}")
            scale += 1

    with open("end_of_blocks.lua", "r") as end_of_blocks:
        blocks.write(end_of_blocks.read())