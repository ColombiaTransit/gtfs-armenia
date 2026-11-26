# Armenia GTFS research

Draft v0.1 covers 14 BASA routes. Not for production: historical estimated weekday headways, assumed 05:00–22:00 departure window, incomplete stop coverage. Sources: BASA route catalogue https://www.busesarmenia.com.co/grivera/get-data.php ; geometry https://logirastreo.com/rutas_buses_armenia.php ; vehicle positions https://logirastreo.com/moviles_buses_armenia.php ; OpenStreetMap (ODbL); AMABLE Manual Operativo, February 2025; municipal mobility plan, 2023 operational tables. Keep planned SETP geometries separate. TUCM source: https://tucm.com.co/rutas/ .

Remaining: R9 geometry, R24/R25/R33 frequencies, Expresa variant allocation, Portugalito geometry and schedule; verify R28 second geometry block (7353–7680); validate stops and direction; weekend and holiday service; MobilityData validator; CI; TUCM and COOBURQUIN; GTFS-RT. Do not publish raw vehicle identifiers or depot positions unnecessarily. Source redistribution permissions must be checked.

Draft route headways (minutes): R1 9, R2 12, R3 20, R4 9, R5 18, R6 19, R7 26, R18 10, R28 10, R31 40, R32 20, R35 6, R36 8, R37 14.
