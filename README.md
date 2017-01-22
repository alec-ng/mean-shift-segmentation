This script uses the [pymeanshift](https://github.com/fjean/pymeanshift) library which implements the mean shift algorithm described by the paper [Mean shift: a robust approach toward feature space analysis](http://ieeexplore.ieee.org/document/1000236/). 

**Requirements**

- One image of just the background without the human subject
- One image of the background with the human subject
- Both images should be taken on the same plane, ideally with a tripod for proper alignment

**Algorithm**

- Perform mean shift to obtain clusters in both the background and human image
- Analyze the clusters found in the segmented human and background images. For each cluster, determine the average RBG values, as well as the average x/y coordinate  
- Segment human clusters that match up with background clusters (based on comparing clusters on avg RBG and X/Y coords, with thresholds)

**Tuning mean-shift parameters**

Spatial Radius: defines the "search circle" from a critical point. All pixels in that "search circle" are checked to see if they belong in the cluster (via range radius value)

- Need a value that is small enough to identify smaller features (e.g. hands), but big enough for bigger features (background)
- Increasing this value exponentially increases the runtime
- Default value: 5

Range Radius: the threshold value in pixel intensities. When taking the aboslute difference in the colour intensities of two pixels, if it is less than the threshold value, the pixels are in the same cluster.

- Need a value that is sensitive enough (lower) to differentiate between clusters that are similar clusters, but general enough (higher) to account for lighting and other parameters that could cause pixels of the same cluster to differ in intensity
- Default value: 15

Density: how many pixels comprise of a cluster. 

- Cannot be too small, else many irrelevant clusters are predicted
- Cannot be too big, or you might not be granular enough to capture smaller clusters
- Default value: 200


**Tuning segmentation parameters** 

Hue Threshold: acceptable difference in average colours between two clusters

- Small enough to differentiate between similar but different clusters, but large enough to picture-to-picture differences (e.g. caused by lighting, shadows)
- Default value: 15

Spatial Threshold: acceptable difference in average X/Y coordinates between two clusters

- Used to gain a rough representation of where each cluster exists spatially
- Default value: 40

**Results**

results/bar

- presence of the black floor bar could not be segmented
- limitation: avg X/Y coords did not pass threshold for the L and R floor bar clusters
- fix: need to address algorithm finding avg X/Y coordinates. a different approach might be needed

results/nobar

- space in between legs could not be segmented
- may suffer from same limitation above, using avg X/Y coordinates


**Limitations**

- Clothing, skin tone and hair of human subject should be substantially different from the immediate background
- Parameters were manually found through trial and error. Automatically generating parameters is not addressed yet


**Example Usage**

`python meanshift.py background.jpg human.jpg 5 15 200 15 40`