#!/usr/bin/env python

# Sets up layers for luminosity masking based
# on procedure in the tutorial found at
# https://www.daviesmediadesign.com/

from gimpfu import *
pdb = gimp.pdb


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
    M = pdb.gimp_channel_copy(D)
    M.name = 'M'
    pdb.gimp_channel_combine_masks(M, L, CHANNEL_OP_INTERSECT, 0, 0)
    image.add_channel(M, -1)

    MM = pdb.gimp_channel_copy(DD)
    MM.name = 'MM'
    pdb.gimp_channel_combine_masks(MM, LL, CHANNEL_OP_INTERSECT, 0, 0)
    image.add_channel(MM, -1)

    MMM = pdb.gimp_channel_copy(DDD)
    MMM.name = 'MMM'
    pdb.gimp_channel_combine_masks(MMM, LLL, CHANNEL_OP_INTERSECT, 0, 0)
    image.add_channel(MMM, -1)

    # Remove our desat layer for cleanliness
    image.remove_layer(desaturated_layer)
    image.active_layer = drawable

    # Create our layer groups
    lights = pdb.gimp_layer_group_new(image)
    lights.name = "Lights"
    # Not sure why this doesn't work:
    # pdb.gimp_image_insert_layer(image, lights, image, -1)
    image.add_layer(lights, -1)

    mids = pdb.gimp_layer_group_new(image)
    mids.name = "Mids"
    image.add_layer(mids, -2)

    darks = pdb.gimp_layer_group_new(image)
    darks.name = "Darks"
    image.add_layer(darks, -3)

    # Now add in our layers with the above channels
    # as layer masks
    Llayer = image.active_layer
    Llayer = layer.copy(True)
    Llayer.name = "L"
    pdb.gimp_image_insert_layer(image, Llayer, lights, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, L)
    mask = Llayer.create_mask(ADD_SELECTION_MASK)
    Llayer.add_mask(mask)

    LLlayer = image.active_layer
    LLlayer = layer.copy(True)
    LLlayer.name = "LL"
    pdb.gimp_image_insert_layer(image, LLlayer, lights, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, LL)
    mask = LLlayer.create_mask(ADD_SELECTION_MASK)
    LLlayer.add_mask(mask)

    LLLlayer = image.active_layer
    LLLlayer = layer.copy(True)
    LLLlayer.name = "LLL"
    pdb.gimp_image_insert_layer(image, LLLlayer, lights, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, LLL)
    mask = LLLlayer.create_mask(ADD_SELECTION_MASK)
    LLLlayer.add_mask(mask)

    Dlayer = image.active_layer
    Dlayer = layer.copy(True)
    Dlayer.name = "D"
    pdb.gimp_image_insert_layer(image, Dlayer, darks, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, D)
    mask = Dlayer.create_mask(ADD_SELECTION_MASK)
    Dlayer.add_mask(mask)

    DDlayer = image.active_layer
    DDlayer = layer.copy(True)
    DDlayer.name = "DD"
    pdb.gimp_image_insert_layer(image, DDlayer, darks, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, DD)
    mask = DDlayer.create_mask(ADD_SELECTION_MASK)
    DDlayer.add_mask(mask)

    DDDlayer = image.active_layer
    DDDlayer = layer.copy(True)
    DDDlayer.name = "DDD"
    pdb.gimp_image_insert_layer(image, DDDlayer, darks, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, DDD)
    mask = DDDlayer.create_mask(ADD_SELECTION_MASK)
    DDDlayer.add_mask(mask)

    Mlayer = layer.copy(True)
    Mlayer.name = "M"
    pdb.gimp_image_insert_layer(image, Mlayer, mids, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, M)
    mask = Mlayer.create_mask(ADD_SELECTION_MASK)
    Mlayer.add_mask(mask)

    MMlayer = image.active_layer
    MMlayer = layer.copy(True)
    MMlayer.name = "MM"
    pdb.gimp_image_insert_layer(image, MMlayer, mids, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, MM)
    mask = MMlayer.create_mask(ADD_SELECTION_MASK)
    MMlayer.add_mask(mask)

    MMMlayer = image.active_layer
    MMMlayer = layer.copy(True)
    MMMlayer.name = "MMM"
    pdb.gimp_image_insert_layer(image, MMMlayer, mids, -1)
    pdb.gimp_image_select_item(image, CHANNEL_OP_REPLACE, MMM)
    mask = MMMlayer.create_mask(ADD_SELECTION_MASK)
    MMMlayer.add_mask(mask)

    # Select none for cleanliness
    pdb.gimp_selection_none(image)


register(
    "luminosity_mask_setup",
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
