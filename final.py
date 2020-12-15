
# Q1.1

# Turning the data x into the standard unit.

# 1.2

masks.take(make_array('Cases', 'Temperature')).scatter('Cases')


#1.5

masks.with_column('Resids', masks.column('Sales') - predict(masks.column('Cases')))


# 1.8



slopes = make_array()
for i in np.arrange(10000):
    boot_tbl = masks.sample(with_replacement=True)
    boot_slope = get_slope(boot_tbl, 'Sales', 'Cases')
    slopes = np.append(slopes, boot_slope)
left = percentile(1, slopes)
right = percentile(99, slopes)
make_array(left, right)



# 5.1

olympics.take('Team', 'Age').group('Team', np.average).sort('Age average').column('Team').item(0)

# 5.2

olympics.where('Year', are.equal_to(2016)).group('Team').num_rows


# 5.3

olympics.where('Year', are.equal_to(2008)).where('Sport', are.equal_to('Snowboarder')).sort('Age', descending=True).column('Name').item(0)

# 5.4

olympics.apply(description, make_array('Name', 'Sport', 'Year'))



all_data = results.drop('Branch', 'Hired')
all_data = all_data.join('Name', encode(recs))
all_data = all_data.with_column('Outcome', results.column('Hired') == 1)


dumpling.with_column('Soup Dumpling Index', (dumpling.column('Meat') + dumpling.column('Soup'))/dumpling.column('Skin'))



def label_proportions(table, neighborhood, label):
  label_dist = table.where('District Shuffled',are.equal_to(neighborhood)).group(label)
  label_counts = label_dist.column(1)
  return label_counts / table.num_rows

def one_test_stat():
  shuffled_Districts = dumpling.sample(with_replacement = False).column('District')
  shuffled_table = dumpling.with_column('District Shuffled', shuffled_Districts)

  props_puxi = label_proportions(shuffled_table,'Puxi','Type')
  props_pudong = label_proportions(shuffled_table,'Pudong','Type')

  return 0.5 * np.sum(abs(props_puxi- props_pudong))
