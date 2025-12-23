def attempt_move(world, entity, dx, dy):
    """Attempts to move entities by dx, dy.
    Returns a result dict describing what happened
    """

    result = {
        "moved": False,
        "blocked": False,
        "tile": None,
        "new_pos": (entity["x"], entity["y"])
    }

    new_x = entity["x"] + dx
    new_y = entity["y"] + dy

    world_map = world["map"]
    height =  len(world_map)
    width = len(world_map[0])

    if new_x < 0 or new_x >= width or new_y < 0 or new_y >= height:
        result["blocked"]=True
        return result
    
    target_tile=world_map[new_y][new_x]
    result["tile"] = target_tile

    if target_tile=='#':
        result["blocked"]=True
        return result
    
    entity["x"]=new_x
    entity["y"]=new_y

    result["moved"]=True
    result["new_pos"]=(new_x,new_y)

    return result