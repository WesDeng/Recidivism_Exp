# Selecting rows based on columns.

us_pop.where('SEX', are.equal_to(0)).where('AGE', are.between(97, 101))
