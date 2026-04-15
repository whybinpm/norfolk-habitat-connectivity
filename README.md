# Project
North Norfolk Habitat Fragmentation Analysis

## Problem statement
Where are the fragmentation gaps between priority habitat 
sites in north Norfolk, and where could wildlife corridors 
realistically be created?

## Data sources
- Natural England Priority Habitat Inventory (PHI)
- SSSI boundaries (Natural England open data)

## Workflow
1. Download and load datasets into QGIS
2. Run buffer analysis around SSSI boundaries
3. Calculate Euclidean distance raster
4. Identify fragmentation gaps
5. Publish web map via Folium

## Known unknowns
- How to handle overlapping buffer zones
- Best cost values to assign to different land cover types

## Definition of done
- Web map published
- Methodology write-up complete
