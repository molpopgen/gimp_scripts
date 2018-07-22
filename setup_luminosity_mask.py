#!/usr/bin/env python

# Sets up layers for luminosity masking based
# on procedure in the tutorial found at
# https://www.daviesmediadesign.com/

from gimpfu import *
pdb = gimp.pdb


def add_layer_group(image, name, location):
    lg = pdb.gimp_layer_group_new(image)
    lg.name = name
    # Not sure why this doesn't work:
    # pdb.gimp_image_insert_layer(image, lg, 0, -1)
    image.add_layer(lg, location)
    return lg


def add_layers_to_groups(image, layer, group, channels, names):
    for channel, name in zip(channels, names):
        layer_copy = image.active_layer
        layer_copy = layer.copy(True)
        layer_copy.name = name
        pdb.gimp_image_insert_layer(image, layer_copy, group, -1)
        pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, channel)
        mask = layer_copy.create_mask(ADD_SELECTION_MASK)
        layer_copy.add_mask(mask)


def setup_luminosity_masking_layers(image, drawable):
    layer = image.active_layer
    desaturated_layer = layer.copy(True)
    desaturated_layer.name = "Desaturated"
    image.add_layer(desaturated_layer, -1)
    pdb.gimp_drawable_desaturate(desaturated_layer, 3)

    # Make a copy of the blue channel.
    # NB: it doesn't matter which channel we copy
    L = pdb.gimp_channel_new_from_component(image, 2, 'L')
    image.add_channel(L, -1)

    # Select all
    pdb.gimp_selection_all(image)

    # Make Dark masks
    pdb.gimp_image_select_item(image, CHANNEL_OP_SUBTRACT, L)
    D = pdb.gimp_selection_save(image)
    D.name = 'D'

    pdb.gimp_image_select_item(image, CHANNEL_OP_SUBTRACT, L)
    DD = pdb.gimp_selection_save(image)
    DD.name = 'DD'

    pdb.gimp_image_select_item(image, CHANNEL_OP_SUBTRACT, L)
    DDD = pdb.gimp_selection_save(image)
    DDD.name = 'DDD'

    # Light masks
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, L)
    pdb.gimp_image_select_item(image, CHANNEL_OP_SUBTRACT, D)
    LL = pdb.gimp_selection_save(image)
    LL.name = 'LL'

    pdb.gimp_image_select_item(image, CHANNEL_OP_SUBTRACT, D)
    LLL = pdb.gimp_selection_save(image)
    LLL.name = 'LLL'

    # Now, our mids
    M = pdb.gimp_channel_copy(L)
    M.name = 'M'
    image.add_channel(M, -1)
    pdb.gimp_drawable_invert(M, 1)
    pdb.gimp_channel_combine_masks(M, D, CHANNEL_OP_INTERSECT, 0, 0)

    MM = pdb.gimp_channel_copy(LL)
    MM.name = 'MM'
    image.add_channel(MM, -1)
    pdb.gimp_drawable_invert(MM, 1)
    pdb.gimp_channel_combine_masks(MM, DD, CHANNEL_OP_SUBTRACT, 0, 0)

    MMM = pdb.gimp_channel_copy(LLL)
    MMM.name = 'MMM'
    image.add_channel(MMM, -1)
    pdb.gimp_drawable_invert(MMM, 1)
    pdb.gimp_channel_combine_masks(MMM, DDD, CHANNEL_OP_SUBTRACT, 0, 0)

    # Remove our desat layer for cleanliness
    image.remove_layer(desaturated_layer)
    image.active_layer = drawable

    # Create our layer groups
    lights = add_layer_group(image, "Lights", -1)
    mids = add_layer_group(image, "Mids", -2)
    darks = add_layer_group(image, "Darks", -3)

    # Now add in our layers with the above channels
    # as layer masks
    add_layers_to_groups(
        image, layer, lights, [L, LL, LLL], ['L', 'LL', 'LLL'])
    add_layers_to_groups(
        image, layer, darks, [D, DD, DDD], ['D', 'DD', 'DDD'])
    add_layers_to_groups(
        image, layer, mids, [M, MM, MMM], ['M', 'MM', 'MMM'])
    
    # Select none for cleanliness
    pdb.gimp_selection_none(image)


register(
    "python-fu-setup_luminosity_masking_layers",
    "Set up channels and layers for luminosity masking.",
    "",
    "Kevin Thornton",
    "Kevin Thornton",
    "2018",
    "Luminosity mask setup",
    "",
    [
        (PF_IMAGE, "image", "takes current image", None),
        (PF_DRAWABLE, "drawable", "input layer", None)
    ],
    [],
    setup_luminosity_masking_layers, menu="<Image>/Filters/Generic")

main()
