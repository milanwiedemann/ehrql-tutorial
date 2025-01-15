library(tidyverse)
library(here)

# Read data
df <- read_csv(here("output", "diabetes_dataset.csv"))

# Create histogram
histogram_age <- ggplot(df, aes(age)) +
  geom_histogram()

# Save histogram as .png
ggsave(here("output", "histogram_age.png"), histogram_age)
