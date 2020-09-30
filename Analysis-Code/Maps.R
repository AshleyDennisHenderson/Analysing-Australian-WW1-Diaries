
# This code creates the maps of New Guinea, Gallipoli, Europe & the Middle East used in my thesis

# Ashley Dennis-Henderson
# September 2020


##  Load Packages ----

pacman::p_load(tidyverse, tidytext, pluralize, ggwordcloud, zoo, topicmodels, xtable, lexicon, leaflet, ngram)

#, , ldatuning, tm, corpus, , , ggwordcloud, rJava, lexicon, vader, ngram, rvest, NLP, openNLP, xtable)


# Maps:
pacman::p_load(devtools)
install_github("edzer/sfr")

pacman::p_load(ggplot2, dplyr, rgdal, raster, rworldmap, ggrepel)


## World Map ----

world <- getMap(resolution = "low")  # Load a world map


## Map (New Guinea) ----

# Create tibble containing the place names, longitudes and latitudes for the locations on the New Guinea map. Lat and Long were manually found using Google maps (https://www.google.com/maps).

NG_coord <- tibble(place = c('Alexishafen', 'Herbertshohe', 'Rabaul', 'Port Moresby', 'Kawieng', 'Nauru', 'Madang', 'Kieta', 'Cocos Islands'), 
                   lon = c(-5.118002, -4.350983, -4.200599, -9.443612, -2.575190, -0.530555, -5.221947, -6.218591, -12.168015), 
                   lat = c(145.777717, 152.272023, 152.164307, 147.172060, 150.805786, 166.932749, 145.789046, 155.639577, 96.82187))


# Get required section of world map:

clipper <- as(extent(90, 200, -30, 15), "SpatialPolygons")
proj4string(clipper) <- CRS(proj4string(world))
world_clip <- raster::intersect(world, clipper)

world_clip_f <- fortify(world_clip)


# Plot map with locations:

ggplot() + 
  geom_polygon(data = world_clip_f,
               aes(x = long, y = lat, group = group),
               fill = "#ffe69a", colour = "black") + 
  geom_point(data = NG_coord, 
             aes(x = lat, y = lon), #, color = place
             color = "red",
             size = 1.75) + 
  geom_label_repel(data = NG_coord, aes(x = lat, y = lon, label = place),
                   box.padding   = 0.75, 
                   point.padding = 0.5,
                   segment.color = 'grey50')  + 
  theme(panel.background = element_rect(fill = "#bfeffd", colour = "#bfeffd",
                                        size = 1, linetype = "solid"),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())



## Map (Gallipoli) ----

# Create tibble containing the place names, longitudes and latitudes for the locations on the Gallipoli map. Lat and Long were manually found using google maps (https://www.google.com/maps).

EUR_coord <- tibble(place = c('Achi Baba', 'Gaba Tepe', "Quinn's Post", 'Mudros Harbour', 'Lemnos'), #,'Lone Pine', 'Dardanelles'
                    lat = c(40.105975, 40.200411, 40.238796, 39.872346, 39.934614), #, 40.241802, 40.062975
                    lon = c(26.255617, 26.266626, 26.291627, 25.265428, 25.142140)) #, 26.285206, 26.301593

#EUR_sf <- st_as_sf(EUR_coord, coords = c("lon", "lat"), crs = 4326)  # ?

# Get required section of world map:

world <- getMap(resolution = "low")

clipper <- as(extent(25, 27, 39.25, 41.25), "SpatialPolygons")
proj4string(clipper) <- CRS(proj4string(world))
world_clip <- raster::intersect(world, clipper)

world_clip_f <- fortify(world_clip)

# Plot map with locations:

p <- ggplot() + 
  geom_polygon(data = world_clip_f,
               aes(x = long, y = lat, group = group),
               fill="#ffe69a", colour = "black") + 
  geom_point(data = EUR_coord, 
             aes(x = lon, y = lat), #, color = place
             color = "red",
             size = 1.75) + 
  geom_label_repel(data = EUR_coord, aes(x = lon, y = lat, label = place),
                   box.padding   = 0.75, 
                   point.padding = 0.5,
                   segment.color = 'grey50')   + 
  theme(panel.background = element_rect(fill = "#bfeffd", colour = "#bfeffd",
                                        size = 1, linetype = "solid"),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())



clipper <- as(extent(10, 60, 25, 50), "SpatialPolygons")
proj4string(clipper) <- CRS(proj4string(world))
world_clip <- raster::intersect(world, clipper)

world_clip_f <- fortify(world_clip)

# Plot map with locations:

p2 <- ggplot() + 
  geom_polygon(data = world_clip_f,
               aes(x = long, y = lat, group = group),
               fill="#ffe69a", colour = "black") + 
  geom_rect(mapping=aes(xmin = 25, xmax = 27, ymin = 39.25, ymax = 41.25), 
            color="red", alpha=0.5) + 
  theme(panel.background = element_rect(fill = "#bfeffd", colour = "#bfeffd",
                                        size = 1, linetype = "solid"),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank())



p2 + annotation_custom(ggplotGrob(p), xmin = 30, xmax = 60, ymin = 25, ymax = 40)


## Map (Europe) ----

# Create tibble containing the place names, longitudes and latitudes for the locations on the Europe map. Lat and Long were manually found using Google maps (https://www.google.com/maps).

EUR_coord <- tibble(place = c('Bapaume', 'Ypres', 'Poperinghe', 'Villers-Bretonneux', 'Amiens', 'Peronne', 'Witney', 'Bailleul', 'Marcinelle', 'Charleroi', 'Gourdinne', 'Paris', 'Sutton Veny', 'Wiesbaden', 'Tidworth', 'Warminster'), 
                    lat = c(50.104559, 50.848972, 50.854242, 49.868248, 49.892127, 49.933444, 51.785918, 50.737004, 50.395239, 50.411133, 50.290094, 48.856845, 51.177142, 50.077147, 51.241484, 51.203203), 
                    lon = c(2.8449448, 2.878953, 2.727810, 2.518953, 2.295622, 2.932520, -1.485336, 2.734671, 4.428218, 4.445965, 4.457628, 2.351288, -2.147593, 8.240791, -1.664458, -2.193895),
                    year = c('1917', '1917', '1917', '1918', '1918', '1918', '1918', '1918', '1919', '1919', '1919', '1919', '1919', '1919', '1919', '1919'))


# Get required section of world map:

clipper <- as(extent(-15, 20, 35, 60), "SpatialPolygons")
proj4string(clipper) <- CRS(proj4string(world))
world_clip <- raster::intersect(world, clipper)

world_clip_f <- fortify(world_clip)


# Plot map with locations:

ggplot() + 
  geom_polygon(data = world_clip_f,
               aes(x = long, y = lat, group = group),
               fill = "#ffe69a", colour = "black") + 
  geom_point(data = EUR_coord, 
             aes(x = lon, y = lat, colour = year),
             size = 1.5) + 
  geom_label_repel(data = EUR_coord, aes(x = lon, y = lat, label = place, colour = year),
                   box.padding   = 0.75, 
                   point.padding = 0.5,
                   segment.color = 'grey50')  + 
  theme(panel.background = element_rect(fill = "#bfeffd", colour = "#bfeffd",
                                        size = 1, linetype = "solid"),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank()) +
  labs(color = "Year")




## Map (Middle East) ----

# Create tibble containing the place names, longitudes and latitudes for the locations on the Europe map. Lat and Long were manually found using google maps (https://www.google.com/maps).

ME_coord <- tibble(place = c('Cairo', 'Alexandria', 'Qatia', 'Tell el Kebir', 'Suez Canal', 'El Arish'), 
                   lat = c(30.044878, 31.202042, 30.952627, 30.475712, 30.567232, 31.132295), 
                   lon = c(31.237796, 29.922763, 32.746500, 31.914368, 32.335614, 33.803694),
                   year = c('1915/1916', '1915', '1916', '1916', '1916', '1916'))


# Get required section of world map:

world <- getMap(resolution = "low")

clipper <- as(extent(20,40,20,40), "SpatialPolygons")
proj4string(clipper) <- CRS(proj4string(world))
world_clip <- raster::intersect(world, clipper)

world_clip_f <- fortify(world_clip)

# Plot map with locations:

ggplot() + 
  geom_polygon(data = world_clip_f,
               aes(x = long, y = lat, group = group),
               fill = "#ffe69a", colour = "black") + 
  geom_point(data = ME_coord, 
             aes(x = lon, y = lat, colour = year),
             size = 1.5) + 
  geom_label_repel(data = ME_coord, aes(x = lon, y = lat, label = place, colour = year),
                   box.padding   = 0.75, 
                   point.padding = 0.5,
                   segment.color = 'grey50')  + 
  theme(panel.background = element_rect(fill = "#bfeffd", colour = "#bfeffd",
                                        size = 1, linetype = "solid"),
        panel.grid.major = element_blank(), 
        panel.grid.minor = element_blank()) +
  labs(color = "Year")