from src.salmon_etl import limpiar_registro


def test_registro_valido():
    registro = {
        "plant": "Hitra",
        "date": "2026-08-20",
        "tons": "125.5",
        "quality": "A"
    }

    limpio, error = limpiar_registro(registro)

    assert limpio["planta"] == "HITRA"
    assert limpio["toneladas"] == 125.5
    assert error is None

def test_registro_sin_toneladas():
    registro = {
        "plant": "Hitra",
        "date": "2026-08-21",
        "tons": None,
        "quality": "A"
    }
    limpio, error = limpiar_registro(registro)

    assert limpio is None
    assert error == "falta tons"