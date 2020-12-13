# Selecting rows based on columns.

us_pop.where('SEX', are.equal_to(0)).where('AGE', are.between(97, 101))

# Getting the name of the item that has the highest value in some attribute.

item_name = tbl.sort('Attribute', descending=True).column('Name').item(0)

# Group Table

tbl_average = tbl.group(make_array('Name', 'item_name'), np.mean).
                    select('Name', 'item_name', 'Overall average')

# Pivot Table

tbl_pivot = tbl.pivot('to_column', 'to_row', 'value', function )


# Bootstrapping:
# Treat the original sample as if it were the population.
# Draw from the sample, at random with replacement,
# the same number of times as the original sample size.

resample_1 = our_sample.sample()

# Middle 95% confidence interval.

left = percentile(2.5, bstrap_medians)
right = percentile(97.5, bstrap_medians)

# Sample from distribution.

probabilities = make_array(0.5, 0.5)
proportions = sample_proportions(10, probabilities)
num_heads = proportions.item(0)*10

# Calculate P value

p_value = np.count_nonzero(test_stats_under_null > observed_statistic)/tbl.num_rows

# Shuffled labels.

shuffled_labels = tbl.sample(with_replacement = False).column(0)
original_and_shuffled = tbl.with_column('Shuffled Label', shuffled_labels


# A/B Testing.
