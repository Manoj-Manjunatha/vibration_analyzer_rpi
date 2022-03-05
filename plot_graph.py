import pandas as pd
from matplotlib import pyplot as plt


def plot_graph():
	filename = 'vacuum_cleaner_accelerometer_data_5s_1646496492.067087.csv'
	df = pd.read_csv(filename, header=None, usecols=[0, 1, 2])
	# df = df[df[0] < '2022-03-05 21:14:04.994648']
	# print(df)
	time = pd.to_datetime(df[0], format='%Y-%m-%d %H:%M:%S.%f')
	x = df[1]
	y = df[2]
	fig, axs = plt.subplots(2, 1)				# Two rows (1 for x and 1 for y data), 1 Column.
	axs[0].plot(time, x)
	axs[0].set_ylabel('Accel x')
	axs[0].set_xlabel('time')

	axs[1].plot(time, y)
	axs[1].set_ylabel('Accel y')
	axs[1].set_xlabel('time')

	plt.show()


if __name__ == '__main__':
	plot_graph()
