import numpy as np
from sklearn import metrics

# To calculate the area under the curve. The area difference two curve is measured.
# One of the curve is plotted using the data from the Aggregated System Demand
# Vs Individual Smart Meter Data

y = np.array([1, 1, 2, 2])
#pred = np.array([0.1, 0.4, 0.35, 0.8])
pred = np.array([1, 1, 2, 2])

fpr, tpr, thresholds = metrics.roc_curve(y, pred, pos_label=2)
a = metrics.auc(fpr, tpr)
print(a)