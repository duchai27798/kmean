import matplotlib.pyplot as ptl
from sklearn.cluster import KMeans
import numpy as np

img = ptl.imread('assets/img.jpeg')

width = img.shape[0]
height = img.shape[1]

img = img.reshape(width * height, 3)

kmeans = KMeans(n_clusters=10).fit(img)

labels = kmeans.predict(img)
clusters = kmeans.cluster_centers_

img2 = np.zeros_like(img)

for i in range(len(img2)):
    img2[i] = clusters[labels[i]]

ptl.imshow(img2.reshape(width, height, 3))
ptl.show()
