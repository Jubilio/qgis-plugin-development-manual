# Snapping strategy

1. Try `canvas.snappingUtils().snapToMap(point)`.
2. If no valid match is returned, iterate visible line and polygon layers.
3. Convert the map point and tolerance into the layer CRS.
4. Query `nearestVertex` first.
5. Query `nearestEdge` only when no vertex candidate exists.
6. Transform the selected point back to the project CRS.
7. Store type and distance for audit.
