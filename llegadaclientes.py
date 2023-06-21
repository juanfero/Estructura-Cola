import tkinter as tk
import random
import math


class Simulation:
    def __init__(self):
        self.customers_served = [0, 0]  # Cantidad de clientes atendidos por cada caja
        self.customers_left = 0  # Cantidad de clientes que se marcharon sin hacer compras
        self.total_waiting_time = 0  # Tiempo total de espera de los clientes en cola
        self.queue = []  # Cola de clientes esperando ser atendidos

    def run_simulation(self, simulation_time, service_rate, arrival_rate):
        # Reiniciar los atributos de la simulación
        self.customers_served = [0, 0]
        self.customers_left = 0
        self.total_waiting_time = 0
        self.queue = []

        # Calcular el tiempo promedio de llegada y de servicio
        arrival_time = 60 / arrival_rate
        service_time = 60 / service_rate

        # Configurar el contador de tiempo
        clock = 0
        customer_counter = 1

        while clock <= simulation_time:
            if len(self.queue) < 6:
                self.queue.append(customer_counter)
                customer_counter += 1
            else:
                self.customers_left += 1

            if random.random() <= arrival_time:
                if len(self.queue) < 6:
                    self.queue.append(customer_counter)
                    customer_counter += 1
                else:
                    self.customers_left += 1

            if self.queue:
                if random.random() <= service_time:
                    customer = self.queue.pop(0)
                    cashier_index = random.randint(0, 1)
                    self.customers_served[cashier_index] += 1
                    self.total_waiting_time += clock * service_time


            clock += 1

    def get_average_waiting_time(self):
        if sum(self.customers_served) == 0:
            return 0
        return self.total_waiting_time / sum(self.customers_served)


class GUI:
    def __init__(self, root):
        self.root = root
        self.simulation = Simulation()

        self.simulation_time_var = tk.StringVar()
        self.service_rate_var = tk.StringVar()
        self.arrival_rate_var = tk.StringVar()

        self.setup_gui()

    def setup_gui(self):
        self.root.title("Simulación de Cola en Restaurante")

        # Etiquetas entrada de parámetros
        tk.Label(self.root, text="Tiempo de Simulación:").grid(row=0, column=0, sticky=tk.E)
        tk.Label(self.root, text="Tasa de Servicio (clientes/hora):").grid(row=1, column=0, sticky=tk.E)
        tk.Label(self.root, text="Tasa de Llegada (clientes/hora):").grid(row=2, column=0, sticky=tk.E)

        # Campos de entrada
        tk.Entry(self.root, textvariable=self.simulation_time_var).grid(row=0, column=1)
        tk.Entry(self.root, textvariable=self.service_rate_var).grid(row=1, column=1)
        tk.Entry(self.root, textvariable=self.arrival_rate_var).grid(row=2, column=1)
        # Botón de simulación
        tk.Button(self.root, text="Simular", command=self.run_simulation).grid(row=3, column=0, columnspan=2)

        # Resultados
        tk.Label(self.root, text="Resultados:").grid(row=4, column=0, sticky=tk.W)
        tk.Label(self.root, text="Clientes atendidos por caja:").grid(row=5, column=0, sticky=tk.W)
        tk.Label(self.root, text="Clientes que se marcharon sin comprar:").grid(row=6, column=0, sticky=tk.W)
        tk.Label(self.root, text="Tiempo promedio en cola (min):").grid(row=7, column=0, sticky=tk.W)

        self.customers_served_label = tk.Label(self.root, text="")
        self.customers_served_label.grid(row=5, column=1, sticky=tk.W)

        self.customers_left_label = tk.Label(self.root, text="")
        self.customers_left_label.grid(row=6, column=1, sticky=tk.W)

        self.average_waiting_time_label = tk.Label(self.root, text="")
        self.average_waiting_time_label.grid(row=7, column=1, sticky=tk.W)

    def run_simulation(self):
        simulation_time = int(self.simulation_time_var.get())
        service_rate = float(self.service_rate_var.get())
        arrival_rate = float(self.arrival_rate_var.get())

        self.simulation.run_simulation(simulation_time, service_rate, arrival_rate)

        self.customers_served_label.config(text=str(self.simulation.customers_served))
        self.customers_left_label.config(text=str(self.simulation.customers_left))
        self.average_waiting_time_label.config(text=str(math.ceil(self.simulation.get_average_waiting_time())))


if __name__ == "__main__":
    root = tk.Tk()
    gui = GUI(root)
    root.mainloop()
