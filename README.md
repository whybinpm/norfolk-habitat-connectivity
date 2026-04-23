# Norfolk Habitat Connectivity Analysis

## Problem statement
North Norfolk contains some of England's most important coastal and wetland 
habitats, yet significant fragmentation exists between designated sites. This 
project analyses the spatial connectivity between Sites of Special Scientific 
Interest (SSSIs) in North Norfolk, identifies fragmentation gaps, and maps 
priority habitat distribution to inform potential wildlife corridor 
opportunities. The analysis is contextualised within the Norfolk Local Nature 
Recovery Strategy (LNRS), adopted November 2025.

## Live interactive map
[View the interactive map here](https://whybinpm.github.io/norfolk-habitat-connectivity/outputs/norfolk_habitat_map.html)

## Data sources
| Dataset | Source | Licence |
|---|---|---|
| Sites of Special Scientific Interest | Natural England (data.gov.uk) | Open Government Licence |
| Priority Habitat Inventory (England) | Natural England (data.gov.uk) | Open Government Licence |
| Local Authority District Boundaries | ONS Geoportal | Open Government Licence |

## Methodology

### 1. Data preparation
SSSI and Priority Habitat Inventory datasets were downloaded as national 
datasets and clipped to the North Norfolk district boundary using QGIS. All 
vector layers were processed in EPSG:27700 (British National Grid).

### 2. Euclidean distance analysis
The clipped SSSI layer was rasterized at 50 metre resolution using QGIS 
Rasterize (Vector to Raster). A Euclidean distance raster was then produced 
using the QGIS Proximity (Raster Distance) tool with georeferenced coordinate 
units, generating a continuous surface where each cell value represents the 
straight-line distance in metres to the nearest SSSI. The output was clipped 
to the North Norfolk boundary.

### 3. Fragmentation gap identification
The proximity raster was visually and analytically interpreted to identify 
areas where SSSI connectivity falls below meaningful thresholds. The 250 metre 
buffer distance used in the Norfolk LNRS methodology was used as a reference 
threshold, consistent with the Lawton Principles of expanding and connecting 
existing important habitat sites.

### 4. Priority habitat mapping
The Priority Habitat Inventory was clipped to North Norfolk and styled by 
main habitat type (mainhabs field) to show the distribution of existing 
priority habitats in relation to the fragmentation surface.

### 5. Corridor link analysis
Potential PHI corridor links were identified and zonal statistics calculated 
to characterise habitat types within potential connectivity zones between 
fragmented SSSI patches.

### 6. Interactive web map
All outputs were combined into an interactive web map using Python (GeoPandas, 
Folium). Vector layers were reprojected to WGS84 (EPSG:4326) for web mapping. 
The proximity raster was exported as a styled PNG from QGIS and georeferenced 
using bounds converted from Web Mercator via PyProj. The map was published 
via GitHub Pages.

## Key findings
- North Norfolk's coastal strip contains dense SSSI coverage with strong 
  habitat connectivity, particularly around Wells-next-the-Sea, Cley, and 
  the Broads fringe.
- Significant fragmentation gaps exist in the interior of the district, 
  particularly in the Aylsham corridor and areas south of the coastal strip, 
  where distances between SSSIs exceed several kilometres.
- Priority habitats including deciduous woodland, lowland fens, and coastal 
  and floodplain grazing marsh are distributed across the district but are 
  concentrated along watercourses and the coast.
- Potential corridor link zones align broadly with ACB areas identified in 
  the Norfolk LNRS, suggesting opportunities for targeted habitat creation 
  in the fragmentation gap zones identified by this analysis.

## Limitations
- Euclidean distance analysis measures straight-line distance only and does 
  not account for land use, terrain, or barriers such as roads and urban areas. 
  A cost surface analysis would provide a more ecologically realistic model of 
  connectivity (planned for project 2).
- The Priority Habitat Inventory may contain classification errors or outdated 
  boundaries in some areas.
- Species-specific dispersal distances have not been modelled — the analysis 
  treats all species as having equivalent connectivity requirements.
- The proximity raster was produced at 50 metre resolution which may 
  underrepresent small habitat patches.

## Tools and technologies
- QGIS 3.x — spatial analysis, raster processing, data preparation
- Python 3.10 — GeoPandas, Folium, Rasterio, PyProj
- GitHub Pages — web map hosting

## Project structure
