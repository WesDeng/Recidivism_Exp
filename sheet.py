# Selecting rows based on columns.

us_pop.where('SEX', are.equal_to(0)).where('AGE', are.between(97, 101))

# Getting the name of the item that has the highest value in some attribute.

item_name = tbl.sort('Attribute', descending=True).column('Name').item(0)

# Group Table

tbl_average = tbl.group(make_array('Name', 'item_name'), np.mean).
                    select('Name', 'item_name', 'Overall average')

# Pivot Table

tbl_pivot = tbl.pivot('to_column', 'to_row', 'value', function )

# Percentage of voting.

single_percentage = np.count_nonzero(bootstrap.column('Vote')
                                                    == 'Target') / tbl.num_rows


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
original_and_shuffled = tbl.with_column('Shuffled Label', shuffled_labels)


# A/B Testing.

repetitions = 1000
test_stats = make_array()

for i in np.arange(repetitions):
    one_stat = simulate_one_stat()
    test_stats = np.append(test_stats, one_stat)

p_value = np.count_nonzero(test_stats >= observed_statistic)/len(test_stats)


##### K nearest neighbors classification ######


for train_row in train.rows:
    # For each train_row in the train dataset, calculate the distance.
    train_row_feature_array = row_to_array(train_row, features)
    row_distance = distance(test_row_features_array, train_row_feature_array)
    distances = np.append(distances, row_distance)

# Adding the distances to the original table and get the first k rows.

train_with_distances = train.with_column("Distances", distances)
nearest_neighbors = train_with_distances.sort("Distances").take(np.arange(K))
most_common_label = nearest_neighbors.group('school').
                            sort('count', descending=True).
                            column('school').item(0)

# Usecase of minimize function for regression.

def fitting_function(a, b, c): return None

best = miniminze(fitting_function)

a, b, c= best.item(0), best.item(1), best.item(2)
