import sys
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class Process:
    """Clase para representar un proceso"""
    name: str
    arrival_time: int
    burst_time: int
    completion_time: int = 0
    turnaround_time: int = 0
    waiting_time: int = 0

class FCFSScheduler:
    """Implementación del algoritmo FCFS"""
    
    def __init__(self):
        self.processes: List[Process] = []
        self.gantt_chart: List[Tuple[str, int, int]] = []
    
    def add_process(self, name: str, arrival_time: int, burst_time: int):
        """Agregar un proceso al planificador"""
        process = Process(name, arrival_time, burst_time)
        self.processes.append(process)
    
    def sort_by_arrival_time(self):
        """Ordenar procesos por tiempo de llegada (FCFS)"""
        self.processes.sort(key=lambda p: p.arrival_time)
    
    def calculate_times(self):
        """Calcular todos los tiempos del algoritmo FCFS"""
        if not self.processes:
            return
        
        # Ordenar por tiempo de llegada
        self.sort_by_arrival_time()
        
        current_time = 0
        self.gantt_chart = []
        
        for process in self.processes:
            # Si el proceso llega después del tiempo actual, hay tiempo inactivo
            if process.arrival_time > current_time:
                current_time = process.arrival_time
            
            # Tiempo de inicio del proceso
            start_time = current_time
            
            # Tiempo de finalización
            process.completion_time = current_time + process.burst_time
            current_time = process.completion_time
            
            # Tiempo de retorno (Turnaround Time)
            process.turnaround_time = process.completion_time - process.arrival_time
            
            # Tiempo de espera (Waiting Time)
            process.waiting_time = process.turnaround_time - process.burst_time
            
            # Agregar al diagrama de Gantt
            self.gantt_chart.append((process.name, start_time, process.completion_time))
    
    def get_average_times(self) -> Tuple[float, float]:
        """Calcular tiempos promedio"""
        if not self.processes:
            return 0.0, 0.0
        
        total_turnaround = sum(p.turnaround_time for p in self.processes)
        total_waiting = sum(p.waiting_time for p in self.processes)
        
        avg_turnaround = total_turnaround / len(self.processes)
        avg_waiting = total_waiting / len(self.processes)
        
        return avg_turnaround, avg_waiting
    
    def print_gantt_chart(self):
        """Imprimir el diagrama de Gantt"""
        print("\n" + "="*60)
        print("DIAGRAMA DE GANTT")
        print("="*60)
        
        # Línea superior con nombres de procesos
        gantt_line = "|"
        time_line = "0"
        
        for process_name, start_time, end_time in self.gantt_chart:
            process_width = end_time - start_time
            gantt_line += f" {process_name:^{process_width*2-1}} |"
            time_line += f"{'':{process_width*2-1}}{end_time}"
        
        print(gantt_line)
        print(time_line)
        
        # Detalles del diagrama
        print("\nDetalles de ejecución:")
        for process_name, start_time, end_time in self.gantt_chart:
            print(f"• {process_name} comienza en el instante {start_time} y termina en el {end_time}")
    
    def print_results_table(self):
        """Imprimir tabla de resultados"""
        print("\n" + "="*80)
        print("TABLA DE RESULTADOS")
        print("="*80)
        
        header = f"{'Proceso':<10}{'T. Llegada':<12}{'T. Ráfaga':<12}{'T. Finalización':<16}{'T. Retorno':<12}{'T. Espera':<12}"
        print(header)
        print("-" * len(header))
        
        for process in self.processes:
            row = f"{process.name:<10}{process.arrival_time:<12}{process.burst_time:<12}{process.completion_time:<16}{process.turnaround_time:<12}{process.waiting_time:<12}"
            print(row)
        
        # Promedios
        avg_turnaround, avg_waiting = self.get_average_times()
        print("-" * len(header))
        print(f"{'PROMEDIO':<10}{'':<12}{'':<12}{'':<16}{avg_turnaround:<12.1f}{avg_waiting:<12.1f}")
    
    def print_summary(self):
        """Imprimir resumen de resultados"""
        avg_turnaround, avg_waiting = self.get_average_times()
        
        print("\n" + "="*60)
        print("RESUMEN DE RESULTADOS")
        print("="*60)
        print(f"Algoritmo utilizado: FCFS (First Come First Serve)")
        print(f"Número de procesos: {len(self.processes)}")
        print(f"Orden de ejecución: {' → '.join([p.name for p in self.processes])}")
        print(f"Tiempo de retorno promedio: {avg_turnaround:.1f} ms")
        print(f"Tiempo de espera promedio: {avg_waiting:.1f} ms")

def print_banner():
    """Imprimir banner del programa"""
    print("="*60)
    print("    ALGORITMO DE PLANIFICACIÓN FCFS")
    print("    (First Come First Serve)")
    print("="*60)

def get_process_data() -> List[Tuple[str, int, int]]:
    """Obtener datos de procesos del usuario"""
    processes_data = []
    
    print("\nIngrese los datos de los procesos:")
    print("Formato: nombre tiempo_llegada tiempo_rafaga")
    print("Ejemplo: P1 0 8")
    print("Escriba 'fin' para terminar\n")
    
    while True:
        try:
            entrada = input("Proceso: ").strip()
            
            if entrada.lower() == 'fin':
                break
            
            partes = entrada.split()
            if len(partes) != 3:
                print("Error: Debe ingresar exactamente 3 valores (nombre, tiempo_llegada, tiempo_rafaga)")
                continue
            
            nombre = partes[0]
            tiempo_llegada = int(partes[1])
            tiempo_rafaga = int(partes[2])
            
            if tiempo_llegada < 0 or tiempo_rafaga <= 0:
                print("Error: Los tiempos deben ser no negativos y el tiempo de ráfaga debe ser positivo")
                continue
            
            processes_data.append((nombre, tiempo_llegada, tiempo_rafaga))
            print(f"✓ Proceso {nombre} agregado")
            
        except ValueError:
            print("Error: Los tiempos deben ser números enteros")
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
            sys.exit(0)
    
    return processes_data

def load_example_data() -> List[Tuple[str, int, int]]:
    """Cargar datos del ejemplo del ejercicio"""
    return [
        ("P1", 0, 8),
        ("P2", 1, 4),
        ("P3", 2, 2),
        ("P4", 3, 5),
        ("P5", 4, 1)
    ]

def main():
    """Función principal"""
    print_banner()
    
    print("\nSeleccione una opción:")
    print("1. Ingresar datos manualmente")
    print("2. Usar datos del ejemplo del ejercicio")
    print("3. Salir")
    
    while True:
        try:
            opcion = input("\nOpción (1-3): ").strip()
            
            if opcion == "1":
                processes_data = get_process_data()
                break
            elif opcion == "2":
                processes_data = load_example_data()
                print("\n✓ Datos del ejemplo cargados:")
                for name, arrival, burst in processes_data:
                    print(f"  {name}: Llegada={arrival}ms, Ráfaga={burst}ms")
                break
            elif opcion == "3":
                print("¡Hasta luego!")
                sys.exit(0)
            else:
                print("Opción inválida. Seleccione 1, 2 o 3.")
                
        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
            sys.exit(0)
    
    if not processes_data:
        print("No se ingresaron procesos. Terminando programa.")
        return
    
    # Crear planificador y agregar procesos
    scheduler = FCFSScheduler()
    for name, arrival, burst in processes_data:
        scheduler.add_process(name, arrival, burst)
    
    # Calcular tiempos
    scheduler.calculate_times()
    
    # Mostrar resultados
    scheduler.print_gantt_chart()
    scheduler.print_results_table()
    scheduler.print_summary()
    
    print("\n" + "="*60)
    print("¡Cálculo completado exitosamente!")
    print("="*60)

if __name__ == "__main__":
    main()
