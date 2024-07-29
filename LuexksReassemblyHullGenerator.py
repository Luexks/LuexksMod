STARTING_INDEX = 17000
STARTING_SORT = 1

print("Luexks Generator DO NOT FUCK UP YOUR INPUTS")

print("Enter shapes individually, enter nothing to end.\nYou must also enter comma-separated scales for the shape, eg: '1,2,3,4' or '2' or '1,3,10'")
shapes = []
shapes_scales = []
while True:
    new_shape = input("Shape\t>")
    if new_shape == "":
        break
    shapes.append(new_shape)
    new_scales = [""]
    new_scales_input = input("Scales\t>")
    scale_index = 0

    for i in range(len(new_scales_input)):
        if new_scales_input[i] == ",":
            new_scales.append("")
            scale_index += 1
            continue

        new_scales[scale_index] += new_scales_input[i]

    shapes_scales.append(new_scales)

for i in range(len(shapes)):
    print(shapes[i], shapes_scales[i])

group = input("Enter group: ")


default_hull_name = input("Enter default hull name: ")
default_hull_blurb = input("Enter default hull blurb: ")
default_hull_features = input("Enter default hull features (format like 'PALETTE|INVISIBLE'): ")
default_hull_durability = input("Enter default hull durability: ")
default_hull_density = input("Enter default hull density: ")
default_hull_growRate = input("Enter default growRate: ")

hull_type_count = int(input("Enter number of hull types: "))

hull_names = [default_hull_name for i in range(hull_type_count)]
hull_blurbs = [default_hull_blurb for i in range(hull_type_count)]
hull_features_s = [default_hull_features for i in range(hull_type_count)]
hull_durabilities = [default_hull_durability for i in range(hull_type_count)]
hull_densities = [default_hull_density for i in range(hull_type_count)]
hull_growRates = [default_hull_growRate for i in range(hull_type_count)]

hull_fillColors = []
hull_fillColor1s = []
hull_lineColors = []

for i in range(hull_type_count):
    hull_fillColors.append(input(f"Hull Type {str(i + 1)}\n\tEnter fillColor: "))
    hull_fillColor1s.append(input("\tEnter fillColor1: "))
    hull_lineColors.append(input("\tEnter lineColor: "))
    if i != 0:
        if input("Enter something (not nothing) if this hull type should have any other different stats: ") != "":
            hull_name = input("Enter something for hull name (entering nothing doesn't)")
            if hull_name != "":
                hull_names[i] = hull_name

            hull_blurb = input("Enter something for hull blurb (entering nothing doesn't)")
            if hull_blurb != "":
                hull_blurbs[i] = hull_blurb

            hull_features = input("Enter something for hull features (entering nothing doesn't)")
            if hull_features != "":
                hull_features_s[i] = hull_features

            hull_durability = input("Enter something for hull durability (entering nothing doesn't)")
            if hull_durability != "":
                hull_durabilities[i] = hull_durability

            hull_density = input("Enter something for hull density (entering nothing doesn't)")
            if hull_density != "":
                hull_densities[i] = hull_density

            hull_growRate = input("Enter something for hull growRate (entering nothing doesn't)")
            if hull_growRate != "":
                hull_growRates[i] = hull_growRate



# Reset the file this way because fuckit, if god told me how to write this better, i would do it.
blocks = open("to_be_appended_blocks.lua", "w")
blocks.write("")
blocks.close()

blocks = open("to_be_appended_blocks.lua", "a")

blocks.write(f"--Hull made with the help of Luexks' hull generator\n{{\n\t{{{STARTING_INDEX}\n\t\tname=\"{hull_names[0]}\"\n\t\tblurb=\"{hull_blurbs[0]}\"\n\t\tfeatures={hull_features_s[0]}\n\t\tgroup={group}\n\t\tdurability={hull_durabilities[0]}\n\t\tdensity={hull_densities[0]}\n\t\tgrowRate={hull_growRates[0]}\n\t\tfillColor=0x{hull_fillColors[0]}\n\t\tfillColor1=0x{hull_fillColor1s[0]}\n\t\tlineColor=0x{hull_lineColors[0]}\n\n\t\tsort={str(STARTING_SORT)}\n\t\tshape={shapes[0]}\n\t\tscale={shapes_scales[0][0]}\n\t}}")
extended_block_alpha = STARTING_INDEX
extended_block_alpha_just_redefined = True
block_index = 1
for hull_type in range(hull_type_count):
    if not extended_block_alpha_just_redefined:
        blocks.write(f"\n\t{{{str(STARTING_INDEX + block_index)},extends={str(STARTING_INDEX)},durability={hull_durabilities[hull_type]}.00001,sort={str(STARTING_SORT + len(shapes) * hull_type)},shape={shapes[0]},scale={shapes_scales[0][0]}")

        if hull_names[hull_type] != default_hull_name:
            blocks.write(f",name=\"{hull_names[hull_type]}\"")
        if hull_blurbs[hull_type] != default_hull_blurb:
            blocks.write(f",blurb=\"{hull_blurbs[hull_type]}\"")
        if hull_features_s[hull_type] != default_hull_features:
            blocks.write(f",features={hull_features_s[hull_type]}")
        # Durability does not need to be handled in this block
        if hull_densities[hull_type] != default_hull_density:
            blocks.write(f",density={hull_densities[hull_type]}")
        if hull_growRates[hull_type] != default_hull_growRate:
            blocks.write(f",growRate={hull_growRates[hull_type]}")

        blocks.write(f",fillColor=0x{hull_fillColors[hull_type]},fillColor1=0x{hull_fillColor1s[hull_type]},lineColor=0x{hull_lineColors[hull_type]}}}")

        extended_block_alpha = STARTING_INDEX + block_index
        extended_block_alpha_just_redefined = True
        block_index += 1

    for shape_index in range(len(shapes)):
        if not extended_block_alpha_just_redefined:
            blocks.write(f"\n\t{{{str(STARTING_INDEX + block_index)},extends={str(extended_block_alpha)},durability={hull_durabilities[hull_type]}.00001,sort={str(STARTING_SORT + len(shapes) * hull_type + shape_index)},shape={shapes[shape_index]},scale={shapes_scales[shape_index][0]}}}")
            block_index += 1
        else:
            extended_block_alpha_just_redefined = False
        extended_block_beta = block_index
        for shape_scale_index in shapes_scales[shape_index][1:]: # SHUT THE FUCK UP
            blocks.write(f"\n\t{{{str(STARTING_INDEX + block_index)},extends={str(STARTING_INDEX + extended_block_beta - 1)},durability={hull_durabilities[hull_type]}.00001,scale={shape_scale_index}}}")
            block_index += 1

blocks.write("\n}")
blocks.close()

