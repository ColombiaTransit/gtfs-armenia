# Intermunicipal service research

Provisional decisions from research discussion; original documents still need archival verification.

| Route | Headway | Departure window | Evidence and uncertainty |
|---|---|---|---|
| R9 | 12 min | 06:00–19:00 | 2023 fleet/cycle estimate (8 vehicles, 96 min); window from historical 2012/2018 registers. Current 2026 detour and 44.76 km geometry require operational verification. |
| R33 | 23 min | 05:00–22:00 | Historical 45 departures per day in 2021/2022, ordinary and holiday; assumed window, direction/dispatch definition unverified. Geometry reaches La Tebaida. |
| R24/R25 | Unknown | Unknown | Armenia–Calarca corridor historical 6 min, 05:00–21:00 (2016), multiple operators; do not assign corridor frequency to individual variants. |

Historical BASA intermunicipal authorizations to locate: 01031 (1992), 03338 (1993), 004 (2011). Historical departure points: Calle 35 Carrera 23–24, Calarca (R24/R25); Calle 26, La Tebaida (R33). No verified current operator timetable yet. Keep these estimates separate from confirmed schedules. Generator unchanged pending explicit implementation and geometry/stop review.

## Further research

Ficha Basica Municipal 2022, pp. 125–128, source Terminal de Transportes de Armenia (2021), lists Armenia–Calarca dispatches ordinary/holiday: CMCC 46/46, COOBURQUIN 71/71, COOMOCAL 164/164, COOTRAFUN 54/54. BASA Calarca routes are not listed; BASA La Tebaida is 45/45. These are terminal statistics and cannot establish BASA R24/R25 frequencies. The 2021 and 2022 figures may refer to the same underlying reporting year, not independent observations. Source: https://www.scribd.com/document/995954943/Ficha-Basica-Municipal-2022

Municipal mobility plan identifies R24 and R25 as separate interurban routes: https://www.armenia.gov.co/wp-content/uploads/2024/02/1Plan_de_Movilidad_Sostenible_y_Segura.pdf . Archived BASA geometry shows R24 via Avenida Bolivar and R25 via Avenida Centenario. Keep both distinct. Calarca historical planning regulation article 109 describes permitted streets but not frequencies: https://tramites1.suit.gov.co/registro-web/suit_descargar_archivo?A=125041 . No confirmed BASA-specific frequency found. Do not extrapolate other operators' dispatch counts.

## Targeted operator and local research (2026-11-26)

User confirmed BASA website API supplies route descriptions only, no additional timetable data. Ministerial resolution search and realtime measurement are parked. No verified R24/R25 headways or departure windows found in indexed operator communications or local news.

- Universidad La Gran Colombia transport study, table 35: indexed R24 frequency cells blank; full PDF fetch timed out: https://www.ulagrancolombia.edu.co/sede/armenia/files/editorial/Transporte_publico.pdf
- Calarca road works report (2025-10-03), BASA detours from Carrera 25 to Carrera 27: https://quindionoticias.com/comenzo-la-rehabilitacion-de-la-carrera-25-cierres-viales-y-desvios-durante-los-proximos-seis-meses-en-calarca/ . Current detour status unverified.
- Local reporting (2026-01-21), irregular corridor frequencies, no route-specific values: https://cronicadelquindio.com/quindio/usuarios-cuestionan-alza-del-transporte-intermunicipal-en-el-quindio/
- Official Coopcacique schedules: https://www.coopcacique.com/ — Avenida Colon–Gran Colombia 05:00–21:12 / 3 min; Ruta Terminal 05:10–19:42 / 12 min; Calarca–Aborigenes Armenia 05:40–21:00 / 12 min. Day types and direction not specified. Separate operator; do not use these for BASA. Future expansion candidate.
- BASA contact form https://www.busesarmenia.com.co/contactenos and published contact basa@busesarmenia.com.co; direct timetable inquiry remains an option, not sent.

## Future GTFS-Realtime (parked)

BasaMaps vehicle endpoint https://logirastreo.com/moviles_buses_armenia.php is a candidate for GTFS-RT VehiclePositions. Before implementation verify usage/redistribution permission, timestamps/freshness, stable non-sensitive vehicle identifiers, route mapping (especially shared Expresa identifier), direction and shape matching. TripUpdates require reliable trip assignment and predictions; not established. No polling workflow or realtime implementation now.
