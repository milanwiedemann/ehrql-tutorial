from ehrql import show, create_dataset, codelist_from_csv
from ehrql.tables.core import patients, clinical_events

index_date = "2024-03-31"

dataset = create_dataset()

# Patient is alive

# Patient is aged 17 years or older

# Patient has unresolved diagnosis of diabetes

show(patients)