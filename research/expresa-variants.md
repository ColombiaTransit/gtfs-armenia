# BASA Expresa variants

## TransCAD model search (2026-11-26)

Exact filename MT4p_Armenia.zip and model name searched, as well as municipal and Universidad del Quindío publications. No public download located. Manual confirms filename. Municipal interadministrative contract 2023-0006 identifies the project. References:
- https://www.armenia.gov.co/wp-content/uploads/2024/02/Plan_de_Movilidad_Sostenible_y_Segura.pdf
- https://www.armenia.gov.co/hoy-mesa-de-participacion-ciudadana-con-la-poblacion-narp-muevete-armenia-hacia-una-movilidad-sostenible-y-segura
- https://www.uniquindio.edu.co/noticias/publicaciones/5120/uq-realizo-el-plan-maestro-de-movilidad-sostenible-y-segura-de-armenia/

Park model search and R24/R25 pending better evidence. Realtime polling remains parked.

## Shape comparison

Source: data/shapes.json, source array order, approximate local planar distance (111000 m/degree longitude, 110600 m/degree latitude). Length-weighted sampling at <=10 m intervals, point-to-segment distance <=30 m to the other shape, ignoring direction. This measures geometric proximity, not identical ordered corridors.

| Shape ID | Points | Length km | Length within 30 m of other | Start/end area | Max segment m |
|---|---:|---:|---:|---|---:|
| Expresa | 285 | 23.969 | 12.987 km (54.18%) | Ciudadela Simón Bolívar | 231 |
| Expresa Gib | 365 | 26.607 | 11.762 km (44.21%) | Gibraltar | 240 |

Both use central/northern Avenida Bolívar; Expresa uses Bosques de Pinares and Avenida del Arriero; Expresa Gib uses Gibraltar and Carrera 19, including a northern Centenario segment. Distinct loops; keep separate routes. Mean length 25.288 km is close to the 25 km in the 2023 operational table, but does not prove that the table covers both. Combined historical estimate: 98 min / 3 buses = 32.67 min, rounded up to 33 min; equal split would be 66 min per route, not an observed schedule. Unequal allocation is also possible. Departure windows and day types remain unknown. Do not publish estimates as confirmed, and do not duplicate the aggregate frequency. Generator unchanged.

## Accepted provisional model

User approved equal division of the historical combined headway. Generator now assigns 3960 seconds to each route with exact_times=0, using the historical 98-minute cycle for both. Separate, unverified draft-only modelling choice: 12.5-hour service window derived from 23 programmed combined departures, default opening 05:00, second variant offset 33 minutes, common end 17:30; this is not a confirmed timetable. The weekday-only draft calendar remains unchanged. Weekend/holiday operation remains unknown. See generator report for assumptions. No production publication.
