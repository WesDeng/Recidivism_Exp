# Selecting rows based on columns.

us_pop.where('SEX', are.equal_to(0)).where('AGE', are.between(97, 101))


# Bootstrapping:
# Treat the original sample as if it were the population.
# Draw from the sample, at random with replacement,
# the same number of times as the original sample size.

resample_1 = our_sample.sample()

# Middle 95% confidence interval.

left = percentile(2.5, bstrap_medians)
right = percentile(97.5, bstrap_medians)
