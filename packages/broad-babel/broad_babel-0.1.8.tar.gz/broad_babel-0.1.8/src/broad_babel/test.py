#!/usr/bin/env jupyter

from broad_babel.query import broad_to_standard, export_csv, run_query

query = ("ccsbBroad304_16164", "BRD-K48830578-001-01-9")
# input_column = ["standard_key", "broad_sample", "pert_type", "JCP2022"]
output_column = "*"
run_query(query, input_column="broad_sample", output_column="*")
