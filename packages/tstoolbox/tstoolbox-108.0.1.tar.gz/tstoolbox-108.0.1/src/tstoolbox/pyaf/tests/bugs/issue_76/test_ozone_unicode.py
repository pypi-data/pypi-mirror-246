import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

plt.rcParams["font.family"] = ["Segoe UI Emoji", "SimHei"]

import pyaf.Bench.TS_datasets as tsds
import pyaf.ForecastEngine as autof

b1 = tsds.load_ozone()
df = b1.mPastData

lTimeVar = "月"
lSignalVar = "臭氧"
df[lSignalVar] = df[b1.mSignalVar]
df[lTimeVar] = df[b1.mTimeVar]


lEngine = autof.cForecastEngine()
lEngine

H = b1.mHorizon
lEngine.train(df, lTimeVar, lSignalVar, H)
lEngine.getModelInfo()
print(lEngine.mSignalDecomposition.mTrPerfDetails.head())


lEngine.standardPlots("outputs/issue_76_unicode__ozone")

dfapp_in = df.copy()
dfapp_in.tail()

dfapp_out = lEngine.forecast(dfapp_in, H)
dfapp_out.to_csv("outputs/issue_76_unicode_ozone_apply_out.csv")
print("Forecast Columns ", dfapp_out.columns)
print(dfapp_out.tail(2 * H))
Forecast_DF = dfapp_out[[lTimeVar, lSignalVar, lSignalVar + "_Forecast"]]
print(Forecast_DF.info())
print("Forecasts\n", Forecast_DF.tail(H))

print("\n\n<ModelInfo>")
print(lEngine.to_json())
print("</ModelInfo>\n\n")
print("\n\n<Forecast>")
print(Forecast_DF.tail(2 * H).to_json(date_format="iso"))
print("</Forecast>\n\n")
