from src.salmon_etl import limpiar_registro, transformar_datos


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

def test_toneladas_invalidas():
    registro = {
        "plant": "Froya",
        "date": "2026-08-21",
        "tons": "ERROR",
        "quality": "A"
    }
    limpio, error = limpiar_registro(registro)

    assert limpio is None
    assert error == "tons no tiene formato valido"

def test_tranformar_datos():
    registros = [
        {
            "plant": "Hitra",
            "date": "2026-08-20",
            "tons": "125.5",
            "quality": "A"
        },
        {
            "plant": "Froya",
            "date": "2026-08-21",
            "tons": "ERROR",
            "quality": "B"
        },
        {
            "plant": "Aukra",
            "date": "2026-08-20",
            "tons": "110.2",
            "quality": "A"
        }
    ]

    limpios, rechazados = transformar_datos(registros)

    assert len(limpios) == 2
    assert len(rechazados) == 1
    assert limpios[0]["planta"] == "HITRA"
    assert rechazados[0]["error"] == "tons no tiene formato valido"

def test_toneladas_negativas():
    registro = {
        "plant": "Hitra",
        "date": "2026-08-20",
        "tons": "-150",
        "quality": "A"
    }

    limpio, error = limpiar_registro(registro)

    assert limpio is None
    assert error == "toneladas negativas"

def test_toneladas_nan():
    registro = {
        "plant": "Hitra",
        "date": "2026-08-20",
        "tons": "NaN",
        "quality": "A"
    }

    limpio, error = limpiar_registro(registro)

    assert limpio is None
    assert error == "toneladas no finitas"