import math

VERTEX_ORIENTATION_MULTIPLIERS = [(-1, -1), (-1, 1), (1, 1), (1, -1)]
SHAPE_ID_ROOT = "201923"
SHAPE_ID_SERIAL_LENGTH = 4
TOTAL_SCALE = 10

BLOCK_ID_BASE = 17000
BLOCK_SORT_BASE = 100

SQUARE_SCALE_COUNT = 4
SQUARE_SCALE_FACTOR = TOTAL_SCALE // 2

TRIANGLE_X_SCALE_COUNT = 4
TRIANGLE_X_SCALE_FACTOR = TOTAL_SCALE
TRIANGLE_Y_SCALE_COUNT = 4
TRIANGLE_Y_SCALE_FACTOR = 5

def combine_list_of_lists(list_of_lists: list) -> list:
    output = []
    for list in list_of_lists:
        output += list
    return output

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

def write_scale_format(verts: list[(float, float)], ports: list[(float, str)]) -> None:
    global shapes
    shapes.write("\n\t\t\t{\n\t\t\t\tverts={")
    for vert in verts:
        shapes.write(f"{{{str(vert[0])},{str(vert[1])}}}")
    shapes.write("}\n\t\t\t\tports={")
    for port in ports:
        shapes.write(f"{{{str(port[0])},{port[1]}}}")
    shapes.write("}\n\t\t\t}")

def generate_spaced_ports(vertex_1: tuple[float, float], vertex_2: tuple[float, float], port_spacing: float, side_index: int) -> list[(int, float)]:
    side_length = math.sqrt((vertex_1[0] - vertex_2[0]) ** 2 + (vertex_1[1] - vertex_2[1]) ** 2)
    port_count = math.floor(side_length / port_spacing)
    
    if port_count <= 1:
        return [(side_index, 0.5)]

    # if port_count % 2 == 0: # I guess it works without the code I thought it would need :P
        # return [(side_index, (0.5 - (port_spacing * (port_count / 2 - 0.5)) / side_length + port_index * port_spacing / side_length)) for port_index in range(int(port_count))]
    
    return [(side_index, (0.5 - (port_spacing * (port_count / 2 - 0.5)) / side_length + port_index * port_spacing / side_length)) for port_index in range(int(port_count))]


with open("shapes.lua", "w") as shapes:
    shapes.write("{")

    # Squares
    shapes.write(f"\n\t{{{shape_id(0)}\n\t\t{{")
    for scale in range(1, SQUARE_SCALE_COUNT + 1):
        write_scale_format([(scale * SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][0], scale * SQUARE_SCALE_FACTOR * VERTEX_ORIENTATION_MULTIPLIERS[vertex_orientation][1]) for vertex_orientation in range(4)], combine_list_of_lists([[(side, f"{str(port * 2 + 1)}/{str((scale) * 2)}") for port in range(scale)] for side in range(4)]))
    shapes.write("\n\t\t}\n\t}")

    # Right Triangles
    triangle_count = 0
    triangle_block_data = []
    shapes.write(f"\n\t{{{shape_id(1)}\n\t\t{{")
    for scale_x in range(1, TRIANGLE_X_SCALE_COUNT + 1):
        for scale_y in range(1, TRIANGLE_Y_SCALE_COUNT + 1):
            new_vertices = [(0, 0), (0, scale_y * TRIANGLE_Y_SCALE_FACTOR), (scale_x * TRIANGLE_X_SCALE_FACTOR, 0)]
            triangle_block_data.append((new_vertices[1][1], new_vertices[2][0]))
            write_scale_format(new_vertices, combine_list_of_lists([generate_spaced_ports(new_vertices[0], new_vertices[1], TOTAL_SCALE, 0), generate_spaced_ports(new_vertices[1], new_vertices[2], TOTAL_SCALE, 1), generate_spaced_ports(new_vertices[2], new_vertices[0], TOTAL_SCALE, 2)]))
            triangle_count += 1
            if new_vertices[1][1] >= new_vertices[2][0]:
                break
    shapes.write("\n\t\t}\n\t}\n\t")

    shapes.write(f"\n\t{{{shape_id(2)}{{}}mirror_of={shape_id(1)}}}")

    shapes.write("\n}")

with open("blocks.lua", "w") as blocks:
    with open("start_of_blocks.lua", "r") as start_of_blocks:
        blocks.write(start_of_blocks.read())

    # Squares
    new_block_id()
    new_block_sort()
    for scale in range(SQUARE_SCALE_COUNT - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(BLOCK_ID_BASE)},durability=2.00001,scale={str(scale + 2)}}}")

    # Right Triangles
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},durability=2.00001,shape={shape_id(1)}}}")
    for scale in range(triangle_count - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)}}}")

    # Mirrored Right Triangles
    new_extend_parent_id = new_block_id()
    blocks.write(f"\n\t{{{str(new_extend_parent_id)},extends={str(BLOCK_ID_BASE)},durability=2.00001,shape={shape_id(2)}}}")
    for scale in range(triangle_count - 1):
        blocks.write(f"\n\t{{{str(new_block_id())},extends={str(new_extend_parent_id)},durability=2.00001,scale={str(scale + 2)}}}")

    with open("end_of_blocks.lua", "r") as end_of_blocks:
        blocks.write(end_of_blocks.read())