#!/usr/bin/env python3
"""Script de verificación de integridad para la fachada analítica ChronDate."""

from mesotimes.date import ChronDate

# =========================================================================
# 1. INICIALIZACIÓN DEL NODO CRONOLÓGICO
# =========================================================================
# Instanciamos el hito temporal proporcionado (JD intermedio)
date = ChronDate(1583129.58611)

print("=== INICIANDO AUDITORÍA DE MÉTODOS DE PRESENTACIÓN DE CHRONDATE ===")
print(f"Instancia base creada con éxito: {repr(date)}")
print(f"Llamada implícita (__call__): {date()} JD")

# =========================================================================
# 2. REPORTES INFORMATIVOS GLOBALES Y LUNARES
# =========================================================================

# Semblanza astronómica del firmamento local (Sol, intervalos de lunación y planetas)
print("\n[Test] Ejecutando day_ephemeris()...")
date.day_ephemeris(city="Babylon", ziggurat=0.0)

# Diagnóstico analítico de Delta T, puntos cardinales del año y catálogo de eclipses
print("\n[Test] Ejecutando year_almanac()...")
date.year_almanac(city="Babylon", ziggurat=15.5)

# Reporte mensual de fases lunares y disparo de la reconstrucción de la tablilla
print("\n[Test] Ejecutando month_almanac()...")
date.month_almanac(city="Babylon", full=True)

# Crónica babilónica del mes lunar estructurada como matriz cuneiforme
print("\n[Test] Ejecutando lunar_info()...")
date.lunar_info(city="Babylon", AoV=12.0, uncertainty=0.833)


# =========================================================================
# 3. HORIZONTES, PASOS MERIDIANOS E INTERVALOS CRÍTICOS
# =========================================================================

# Desglose de tránsitos solares y cálculo dinámico de las tres vigilias nocturnas (maṣṣarātu)
print("\n[Test] Ejecutando sun_rise_transit_set()...")
date.sun_rise_transit_set(city="Babylon", ziggurat=0.0)

# Dashboard del día babilónico local (cálculo de puesta a puesta de sol)
print("\n[Test] Ejecutando bab_day_info()...")
date.bab_day_info(city="Babylon")

# Eventos horizontales de la Luna (orto, tránsito y ocaso en UT)
print("\n[Test] Ejecutando moon_rise_transit_set()...")
date.moon_rise_transit_set(city="Babylon")

# Auditoría del intervalo de oposición de Luna Llena en el medio del mes (MI-MUSH)
print("\n[Test] Ejecutando mi_mush()...")
date.mi_mush(city="Babylon")

# Auditoría del intervalo de desaparición del creciente al amanecer (KUR)
print("\n[Test] Ejecutando kur()...")
date.kur(city="Babylon")

# Verificación de los criterios empíricos de visibilidad para el primer creciente (Neomenia)
print("\n[Test] Ejecutando neomenia()...")
date.neomenia(city="Babylon", AoV=12.0)


# =========================================================================
# 4. ALMANAQUES PLANETARIOS INDIVIDUALES (Despachadores)
# =========================================================================
print("\n[Test] Desplegando almanaques analíticos planetarios individuales...")

date.mercury_almanac()
date.venus_almanac()
date.mars_almanac()
date.jupiter_almanac()
date.saturn_almanac()


# =========================================================================
# 5. MATRICES DE OPERADORES MÁGICOS Y ARITMÉTICA TIMELINE
# =========================================================================
print("\n[Test] Verificando consistencia de operadores mágicos y aritmética...")

# Inmutabilidad y Adición
future_date = date + 30
print(f"  Aritmética (+30 días): {repr(future_date)}")

# Sustracción de días y Diferencia absoluta de JDs (retorna float)
past_date = date - 5
days_between = future_date - past_date
print(f"  Aritmética (-5 días) : {repr(past_date)}")
print(f"  Intervalo absoluto entre nodos: {days_between:.5f} días")

# Comparaciones posicionales lógicas
print(f"  Evaluación lógica (==): {date == ChronDate(1583129.58611)}")
print(f"  Evaluación lógica (<) : {past_date < date < future_date}")

# Hashing seguro para colecciones
date_dict = {date: "Babylonian Anchor Context"}
print(f"  Persistencia en estructuras hash: {date_dict[date]}")


# =========================================================================
# 6. RENDERIZADO VISUAL ASCII CLI
# =========================================================================
# Cierre del flujo gráfico con la caché de posiciones horizontales
print("\n[Test] Dibujando gráfico de visibilidad horizontal...")
date.night_at_a_glance(city="Babylon")

# =========================================================================
# 7. ESCANEO DE FASES HELÍACAS (Nuevo Finder integrado)
# =========================================================================
print("\n[Test] Escaneando próximas estaciones helíacas para Venus...")
date.heliacal_phases("Mercury", city="Babylon")

print("\n=== AUDITORÍA FINALIZADA SIN ERRORES DE EXCEPCIÓN DE ESTRUCTURA ===")