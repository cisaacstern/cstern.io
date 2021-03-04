USGS provides a <a href="https://apps.nationalmap.gov/downloader/#/" target="_blank">National Map Download Client</a> for interactively accessing all of their publically available data products. This app replicates that functionality but for a more narrow use-case: downloading 1 arc-second Digital Elevation Models (DEMs) via HTTP request.

Through this exercise, I've come to appreciate inherent bottlenecks in the "download model" of data access (cf. <a href="10.22541/au.160443768.88917719/v2" target="_blank">Ryan Abernathey, Tom Augspurger, Anderson Banihirwe, et al. Cloud-Native Repositories for Big Scientific Data. Authorea. January 19, 2021.</a>). While this approach works well for single DEMs, it falls short in two key dimensions:

<ul class="not-nav">
    <li>
    1. Scaling to a large quantity of DEMs (such as, every DEM for the contiguous US) would require prohibitively large amount of disk space; and,
    </li>
    <li>
    2. Even if we did choose to download all of these files, tiling them together into a form that would allow seamless analysis (presumably, without loading them into memory) remains a major task.
    </li>
</ul>
  
As such, a scalable implementation of this project would likely require a redesign for cloud object storage and/or use of a labeled array format such as Zarr. That being said, the existing functionality is quite useful for streamlining access for single-DEM analyses.