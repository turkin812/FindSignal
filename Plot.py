import matplotlib.pyplot as plt
import numpy as np


class Plotling:
	def __init__(self):
		super().__init__()

	def t_y_ps(self, f1: float, f2: float, f3: float, fd: float, N: int, n0: int, n1: int):
		tstep = 1 / fd
		phase = 2 * np.pi * f1 * tstep * (n0-1)
		list_x = []
		for i in range(0, n0-1):
			list_x.append(np.sin(2 * np.pi * f1 * tstep * i))
		for i in range(0,n1-n0+1):
			list_x.append(np.sin(2 * np.pi * f2 * tstep * i+phase))
		phase += 2 * np.pi * f2 * tstep * (n1-n0+1);
		for i in range(0,N-n1):
			list_x.append(np.sin(2 * np.pi * f3 * tstep * i+phase))
		
		list_t = []
		for i in range (0, N):
			list_t.append(i*tstep)

		list_deviation_x = []
		list_deviation_t=[]
		max_x = 0

		for i in range(2, N-2):
			list_deviation_t.append(i*tstep)
			list_deviation_x.append(abs(list_x[i] - (list_x[i - 1] * (2 * np.cos(2 * np.pi * f2*tstep)) - list_x[i - 2])))
			if (max_x < list_deviation_x[i - 2]):
				max_x = list_deviation_x[i - 2]
		return list_t, list_x, list_deviation_t, list_deviation_x

	def filter(self, N: int, tt: float, TT: float, fd: float, list_deviation_x: list, n0: int, n1: int):
		# Фильтр
		TT = int(TT)
		average_error_t0 = TT + 2
		number_samples = TT * 2 + 1
		average_error_x = []
		average_error_y = []
		out_n0 = 0
		out_n1 = 0
		no_start = True

		for n in range(average_error_t0, N - average_error_t0):
			average_error_x.append(n / fd)
			average_error_sum = 0.0

			# Суммирование значений в окне
			for i in range(-TT, TT+1):
				average_error_sum += list_deviation_x[n + i-2]

			# Среднее значение в окне
			average_error_y.append(average_error_sum / number_samples);

			# Поиск начала и конца
			if (average_error_y[n - average_error_t0] < tt and no_start): 
				out_n0 = n
				no_start = False

			
			if (average_error_y[n - average_error_t0] < tt):
				out_n1 = n
			
		list_threshold_value = []

		# Порог ошибки
		for n in range(0, N):
			list_threshold_value.append(tt)

		out_del_n0 = out_n0
		out_del_n1 = out_n1
		return list_threshold_value, average_error_x, average_error_y,out_del_n0, out_del_n1



	def _plot(self, list_threshold_value:list, list_t: list, list_deviation_t: list, list_x: list, list_deviation_x: list, average_error_x: list, average_error_y: list):
		plt.close()
		fig, ax = plt.subplots(2, 1)
		# plt.figure(figsize=(200, 200))
		ax[0].set(xlabel='', ylabel='A', title='Исходный и обнаруженный сигнал')
		ax[1].set(xlabel='time, s', ylabel='E^2', title='График ошибки')
		ax[0].grid(True)
		ax[1].grid()
		ax[0].plot(list_t, list_x, color = 'b')

		ax[1].plot(list_deviation_t, list_deviation_x, color = 'r')
		
		ax[1].plot(average_error_x, average_error_y, color = 'g')
		ax[1].plot(list_t, list_threshold_value, color = 'b')
		#ax[1].legend((u'Первый график', u'Второй график', u'Третий график'), frameon = 'False')
		#fig.savefig("test.png")
		fig.tight_layout()
		plt.show()

if __name__ == "__main__":
	md = Plotling()