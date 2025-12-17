
class Action:
    def __init__(self, name, action_type, requirements=None, effects=None, penalty=None, limit_per_day=None):
        self.name = name
        self.action_type = action_type
        self.requirements = requirements or {}
        self.effects = effects or {}
        self.penalty = penalty or {}
        self.limit_per_day = limit_per_day

    def is_allowed(self, player):
        for stat, value in self.requirements.items():
            if player.stats.get(stat) < value:
                return False
        return True

    def apply_effects(self, player, multiplier=1.0):
        for stat, value in self.effects.items():
            player.stats.modify(stat, int(value * multiplier))

    def apply_penalty(self, player):
        for stat, value in self.penalty.items():
            player.stats.modify(stat, value)



# =============================
# ACCIONES POSITIVAS
# =============================


caminar_10k = Action(
"Caminar 10k pasos", "positive", effects={"salud": 10, "disciplina": 10}, limit_per_day=1
)


caminar_5k = Action(
"Caminar 5k pasos", "positive", effects={"salud": 5, "disciplina": 5}, limit_per_day=1
)


entrenar = Action(
"Entrenar", "positive", effects={"salud": 8, "disciplina": 8}, limit_per_day=1
)


dormir_bien = Action(
"Dormir bien", "positive", effects={"salud": 6, "disciplina": 6}, limit_per_day=1
)


estudiar_1h = Action(
"Estudiar 1h", "positive", effects={"estudios": 8, "disciplina": 8}, limit_per_day=3
)


leer = Action(
"Leer 30 min", "positive", effects={"estudios": 5, "disciplina": 5}, limit_per_day=2
)


ver_amigo = Action(
"Ver a un amigo", "positive", effects={"amistades": 8, "salud": 5}, limit_per_day=1
)


hablar_bien = Action(
"Hablar bien con alguien", "positive", effects={"amistades": 4}, limit_per_day=2
)


planificar = Action(
"Planificar el día", "positive", effects={"disciplina": 4}, limit_per_day=1
)


no_fumar = Action(
"No fumar en el día", "positive", effects={"disciplina": 8, "salud": 10}, limit_per_day=1
)


tiempos_calidad = Action(
"Tiempo de calidad (pareja)", "positive", effects={"relacion": 7, "felicidad": 5}, limit_per_day=1
)


charla_pareja = Action(
"Charla profunda (pareja)", "positive", effects={"relacion": 4}, limit_per_day=1
)

amor_tiempo = Action(
"Dia con mi bebu", "positive", effects={"relacion": 7, "felicidad": 15}, limit_per_day=1
)

familia_tiempo = Action(
"Compartir tiempo con familia", "positive", effects={"familia": 6}, limit_per_day=1
)


ahorrar = Action(
"Ahorrar dinero", "positive", effects={"economia": 10, "disciplina": 15}, limit_per_day=1
)


# =============================
# ACCIONES ESPECIALES (HABILITADAS)
# =============================


hamburguesa = Action(
"Comer hamburguesa",
"special",
requirements={"salud": 50},
effects={"amistades": 5, "salud": -5, "economia": -5, "disciplina": -3},
penalty={"salud": -15, "disciplina": -5}
)
hamburguesa_conLupi = Action(
"Comer hamburguesa con mi bebu",
"positive",
effects={"salud": -5, "economia": -10, "felicidad": 10, "relacion": 10},
)


viciar = Action(
"Viciar 3h",
"special",
requirements={"disciplina": 25},
penalty={"disciplina": -15}
)
viciar_conamigos = Action(
"Viciar con amigos",
"special",
requirements={"disciplina": 30, "amistades": 40},
effects={"amistades": 7, "disciplina": -5, "salud": -2, "felicidad": 7},
penalty={"disciplina": -10}
)


juntada = Action(
"Juntada a escabiar",
"special",
requirements={"salud": 35, "disciplina": 30},
effects={"amistades": 10, "salud": -7, "economia": -5},
penalty={"salud": -10, "disciplina": -5}
)


# ============================
# ACCIONES NEGATIVAS (NO HABILITADAS)
# ============================
fumar = Action(
    "Fumar un cigarrillo",
    "special",
    requirements={"disciplina": 50},
    effects={"disciplina": -10, "salud": -10},
    penalty={"salud": -8, "disciplina": -6}
)

comer_chatarra = Action(
    "Comer comida chatarra",
    "special",
    requirements={"salud": 35, "economia": 50},
    effects={"salud": -8, "economia": -5},
    penalty={"salud": -10}
)

dormir_mal = Action(
    "Dormir mal",
    "special",
    requirements={"disciplina": 55},
    effects={"salud": -5, "disciplina": -3},
    penalty={"salud": -12, "disciplina": -6}
)
viciar_excesivo = Action(
    "Viciar 6h",
    "special",
    requirements={"disciplina": 55, "amistades": 50},
    effects={"disciplina": -10, "salud": -10},
    penalty={"disciplina": -20}
)

procrastinar = Action(
    "Procrastinar todo el día",
    "special",
    requirements={"disciplina": 60},
    effects={"disciplina": -20, "salud": -5},
    penalty={"disciplina": -25, "salud": -10}
)
colgar_amigo = Action(
    "Colgar a un amigo",
    "special",
    requirements={"amistades": 45},
    effects={"amistades": -5},
    penalty={"amistades": -12}
)

evitar_familia = Action(
    "Evitar a la familia",
    "special",
    requirements={"familia": 55},
    effects={"familia": -7},
    penalty={"familia": -10}
)
gasto_impulsivo = Action(
    "Gasto impulsivo",
    "special",
    requirements={"economia": 40},
    effects={"economia": -10, "disciplina": -5},
    penalty={"economia": -15, "disciplina": -5}
)

pedir_prestado = Action(
    "Pedir plata prestada",
    "special",
    requirements={"economia": 20},
    effects={"economia": 15, "disciplina": -5},
    penalty={"economia": -20}
)
discusion_fuerte = Action(
    "Discusión fuerte con la pareja",
    "special",
    requirements={"relacion": 60},
    effects={"relacion": -10},
    penalty={"relacion": -25}
)
# =============================
# REGISTRO GLOBAL
# =============================


ALL_ACTIONS = [
caminar_10k, caminar_5k, entrenar, dormir_bien,
estudiar_1h, leer,
ver_amigo, hablar_bien,
planificar, no_fumar,
tiempos_calidad, charla_pareja,
familia_tiempo,
ahorrar,
hamburguesa, viciar, juntada,    fumar,
    comer_chatarra,
    dormir_mal,
    viciar_excesivo,
    procrastinar,
    discusion_fuerte,
    colgar_amigo,
    evitar_familia,
    gasto_impulsivo,
    pedir_prestado,
    amor_tiempo, hamburguesa_conLupi,
]