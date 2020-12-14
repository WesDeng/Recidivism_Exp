
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
