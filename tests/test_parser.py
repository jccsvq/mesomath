""" Test for the 75 types of MesoMath output metrological expressions used as input.
"""

import mesomath as mm




def test_parser_consistency(value=11223344):
    # Lista de clases a testear
    classes = [
        mm.Blen,
        mm.Bsur,
        mm.Bvol,
        mm.Bcap,
        mm.Bwei,
        mm.Bbri,
        mm.BsyS,
        mm.BsyG,
    ]

    results = {"pass": 0, "fail": 0, "errors": []}

    for cls in classes:
        print(f"\n--- Testing class: {cls.__name__} ---")

        # 1. Crear objeto base
        try:
            obj_ref = cls(value)
        except Exception as e:
            print(f"Error instantiating {cls.__name__}: {e}")
            continue

        # 2. Generar pool de strings con diferentes formatos
        test_strings = []

        # Guardar estado original de prtsex para restaurarlo
        original_prtsex = getattr(obj_ref, "prtsex", 0)

        for ps in [0, 1]:
            obj_ref.prtsex = ps
            test_strings.append(str(obj_ref))
            # Probar las combinaciones de prtf(frac, dot)
            for frac in [0, 1]:
                for dot in [0, 1]:
                    test_strings.append(obj_ref.prtf(frac, dot))

        # Restaurar
        obj_ref.prtsex = original_prtsex

        # 3. Eliminar duplicados para no repetir tests
        unique_strings = list(set(test_strings))

        # 4. Fase de Assertions
        for s in unique_strings:
            try:
                # Intentamos recrear el objeto desde el string
                obj_new = cls(s)

                if obj_new.dec == value:
                    results["pass"] += 1
                    print(f"  [OK] '{s}'")
                else:
                    results["fail"] += 1
                    err = f"  [FAIL] '{s}' -> Got {obj_new.dec}, expected {value}"
                    print(err)
                    results["errors"].append(err)

            except Exception as e:
                results["fail"] += 1
                err = f"  [CRASH] '{s}' -> Exception: {e}"
                print(err)
                results["errors"].append(err)

    print("\n" + "=" * 30)
    print(f"FINAL REPORT: {results['pass']} Passed, {results['fail']} Failed")
    print("=" * 30)

    assert results["fail"] == 0, "Some tests failed"

    return results


if __name__ == "__main__":
    test_parser_consistency()
