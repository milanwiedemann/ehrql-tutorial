from ehrql import show, create_dataset, codelist_from_csv
from ehrql.tables.core import patients, clinical_events, practice_registrations

index_date = "2024-03-31"

dataset = create_dataset()

# Patient is alive
dataset.is_alive = patients.is_alive_on(index_date)

# Patient is aged 17 years or older 
dataset.age = patients.age_on(index_date)
dataset.aged_17_or_older = dataset.age >= 17

# Patient has unresolved diagnosis of diabetes
diabetes_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dm_cod.csv",
    column="code",
    )

resolved_codes = codelist_from_csv(
    "codelists/nhsd-primary-care-domain-refsets-dmres_cod.csv",
    column="code",
    )

dataset.last_dm_diagnosis_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(diabetes_codes))
    .sort_by("date")
    .where(clinical_events.date <= index_date)
    .last_for_patient()
    .date
)

dataset.last_dm_resolved_date = (
    clinical_events.where(clinical_events.snomedct_code.is_in(resolved_codes))
    .sort_by("date")
    .where(clinical_events.date <= index_date)
    .last_for_patient()
    .date
)

dataset.has_unresolved_diabetes = dataset.last_dm_diagnosis_date.is_not_null() & (
    dataset.last_dm_resolved_date.is_null() | (dataset.last_dm_resolved_date < dataset.last_dm_diagnosis_date)
)

dataset.define_population(dataset.is_alive & dataset.aged_17_or_older & dataset.has_unresolved_diabetes)

show(dataset)
