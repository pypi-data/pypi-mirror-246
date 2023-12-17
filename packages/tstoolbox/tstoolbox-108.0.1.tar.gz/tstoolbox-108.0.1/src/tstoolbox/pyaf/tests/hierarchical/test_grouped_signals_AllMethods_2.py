import datetime

import numpy as np
import pandas as pd
import pyaf.Bench.TS_datasets as tsds
import pyaf.HierarchicalForecastEngine as hautof

# get_ipython().magic('matplotlib inline')

b1 = tsds.load_AU_infant_grouped_dataset()


df = b1.mPastData

lEngine = hautof.cHierarchicalForecastEngine()
lEngine.mOptions.mHierarchicalCombinationMethod = ["BU", "TD", "MO", "OC"]
lEngine.mOptions.mNbCores = 16
lEngine

H = b1.mHorizon

# lEngine.mOptions.enable_slow_mode();
# lEngine.mOptions.mDebugPerformance = True;
lEngine.mOptions.set_active_autoregressions([])
lEngine.train(df, b1.mTimeVar, b1.mSignalVar, H, b1.mHierarchy, None)

lEngine.getModelInfo()
# lEngine.standardPlots("outputs/AU_infant_");

dfapp_in = df.copy()
dfapp_in.tail()

dfapp_out = lEngine.forecast(dfapp_in, H)
# dfapp_out.to_csv("outputs/Grouped_AU_apply_out.csv")
