def relationship_buff(player):
    if player.stats.get("relacion") >= 80:
        return {
            "salud": 1.1,
            "estudios": 1.1,
            "amistades": 1.1,
            "familia": 1.1
        }
    return {}
