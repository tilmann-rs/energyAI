# energyAI

A Python project for loading, preprocessing, analyzing, and forecasting energy generation and consumption data, with a focus on time series modeling using classic and deep learning-based approaches.

- **Data Loading & Preprocessing:** Utilities for cleaning and preparing large-scale energy datasets from ENTSO-E platform.

- **Time Series Forecasting:** Implements classical models (SARIMA, VAR) and deep learning models (Transformers, TimesNet) for forecasting, imputation, anomaly detection, and classification.
- `data_load/preprocess.py` – Data cleaning and transformation.
- `model/simple_tsf.py` – Classical time series models.
- `model/transformer.py` – Transformer-based forecasting and analysis.
- `model/TimesNet.py` – TimesNet deep learning model for time series (see [TimesNet paper](https://openreview.net/pdf?id=ju_Uqw384Oq)).



<br>
<br>

![grafik](https://github.com/user-attachments/assets/6389df4c-14a5-4b88-9993-7b9f7c51880a)

<br>
*Net energy generation by source and consumption over a 24-hour period of ENTSO-E transperancy platform*
<br>
