# Data

The analysis uses the dunnhumby *The Complete Journey* dataset: household-level grocery transactions of about 2,500 frequent shoppers over two years, with household demographics and direct-marketing (campaign) history for some households.

The CSV files are not in this repository (they are git-ignored). Download them and place them in this folder.

| Item | Value |
|---|---|
| Source | dunnhumby, [Source Files](https://www.dunnhumby.com/source-files/) page, entry "The Complete Journey" (the page links a download; it lists no file names, so the names below are the ones the notebooks read) |
| Files | `transaction_data.csv`, `hh_demographic.csv`, `product.csv`, `campaign_table.csv`, `campaign_desc.csv`, `causal_data.csv`, `coupon.csv`, `coupon_redempt.csv` |
| Location | `data/` (the notebooks read `DATA_DIR / "<file>.csv"`, where `DATA_DIR` comes from `config.py`) |
| Size | `transaction_data.csv` is about 135 MB (2,595,732 rows) |

`dunnhumby_data_overview.ipynb` reads all eight files. The analysis notebooks read `transaction_data`, `hh_demographic`, `product`, `campaign_table`, `campaign_desc` and `causal_data`.

Raw files are not included in this repository; download them from the source above.
