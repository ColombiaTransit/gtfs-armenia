# R-PORTUGALITO research

## Confirmed evidence

- BASA catalogue snapshot supplied by user: route ID R-PORTUGALITO, status Activo, vehicle route key PORTUGALITO, shape key PORTUGALITO, colour #40E0D0. The archived 23,364-point shapes.json contains zero records with Portugalito in either route key or description (case-insensitive).
- Municipal mobility plan, Table 13, source BASA/TINTO 2023: one vehicle, cycle 120 min, four programmed runs, 43 km per cycle, 21.5 km/h, 172 km/day. Four cycles are consistent with the distance and eight hours of driving, but departure times, day types and layovers are unknown. See research/basa-operating-parameters-2023.csv.
- El Caimo communal development plan 2020–2023, printed p.43: requested extension of the existing Caimo–Portugalito service's route and operating hours. The document separately requests service for Golconda, Marmato and San Pedro; these should not be presumed to be served by Portugalito. Source: https://www.armenia.gov.co/wp-content/uploads/2022/DESARROLLO_SOCIAL_/PLANES_DE_DESARROLLO_COMUNAL_2020_2023/1._PLAN_DE_DESARROLLO_COMUNAL_SECTOR_RURAL_2_compressed.pdf
- El Caimo rural development plan 2024–2027, traffic/transport priorities: residents of Caimo and Cristales request an increased frequency for Portugalito. This is a request, not an approved new timetable. Source: https://armenia.gov.co/wp-content/uploads/2023_-_Unidad_de_Participacin_Ciudadana/PLAN_DE_DESARROLLO_CORREGIMIENTO_EL_CAIMO.pdf
- Municipality reports rehabilitation of one kilometre of rural road between El Caimo and Portugalito: https://armenia.gov.co/rehabilitacion-de-via-el-caimo-portugalito-mejora-la-movilidad-del-sector . This verifies a road corridor, not the whole bus alignment.
- Both communal plan text extracts were accessible via web indexing; direct PDF screenshot retrieval failed with 403/404. No verified current timetable or complete route description found in public search.

## Next steps / hold

Check whether BASA's website route selector (https://www.busesarmenia.com.co/rutas) returns a Portugalito route description. The text-only indexed page exposes no selection responses. If available, use it and OSM road geometry / GraphHopper to reconstruct and review the approximately 43 km loop; do not infer a city-side terminal or exact path from rural names alone. If there are four fixed daily dispatches, use explicit trips once departure times and day types are known; no automatic 120-minute headway. No realtime API polling. Keep route held in generator until sufficient evidence. No changes to generator in this research pass.

## Existing draft status

Actions run 45859718230 succeeded, and generator log confirms both Expresa variants emitted (17 and 26 candidate stops respectively), with Portugalito held. Successful execution does not by itself prove validator has no notices.


## Official BASA website route description (user-supplied)

Fondo_1

# RPortugalito

Calle 25 entre Carrera 17 y Carrera 16 — Carrera 16 — Calle 26 — Ordenador vial La Cejita — Carrera 19 - Glorieta Tres Esquinas — Calle 51 — Cementerio Jardines de Armenia - Puesto de Policía Granada — Corregimiento El Caimo — La Báscula — Portugalito — La Báscula — Corregimiento El Caimo — Puesto de Policia Granada — Cementerio Jardines de Armenia — Carrera 8 — Club de Caza Tiro y Pesca — Calle 50 — Carrera 18 — Calle 26 — Carrera 17 — Calle 25.

Source: BASA route selector response supplied by user; exact request URL and capture date not independently verified. This resolves the previously unknown city-side terminal and ordered itinerary. The rural corridor is shared in both directions; urban legs differ. Geocode and verify each named waypoint, then route with organization's bus GraphHopper profile, preserving direction and rural road access. Compare complete loop to 43 km historical target, not as a hard constraint. No verified GPS coordinates or exact departure times yet. Four programmed runs and 120-minute cycle do not determine dispatch times. Keep generator hold until geometry and schedule evidence are sufficient.
