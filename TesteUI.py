import PySimpleGUI as sg
import time
import random

def simulate_test_results():
    """Função que simula os resultados dos testes."""
    return {
        'esp_voltage': round(random.uniform(2.9, 3.7), 2),     # Simula tensão entre 2.5V e 3.7V
        'display_voltage': round(random.uniform(2.9, 3.7), 2), # Simula tensão entre 2.5V e 3.7V
        'sensor_voltage': round(random.uniform(2.9, 3.7), 2),  # Simula tensão entre 2.5V e 3.7V
        'oxygen_level': round(random.uniform(85.0, 100.0), 1)  # Simula nível de oxigênio entre 85% e 100%
    }

def evaluate_test_results(results):
    """Função que avalia os resultados dos testes e determina se passam ou falham."""
    esp_pass = 3.0 <= results['esp_voltage'] <= 3.7 and results['esp_voltage'] >= 2.9
    display_pass = 3.0 <= results['display_voltage'] <= 3.7 and results['display_voltage'] >= 2.9
    sensor_pass = 3.0 <= results['sensor_voltage'] <= 3.7 and results['sensor_voltage'] >= 3.0
    oxygen_pass = results['oxygen_level'] >= 85.0

    all_pass = esp_pass and display_pass and sensor_pass and oxygen_pass

    return {
        'esp_pass': esp_pass,
        'display_pass': display_pass,
        'sensor_pass': sensor_pass,
        'oxygen_pass': oxygen_pass,
        'overall_pass': all_pass
    }

def run_tests(window):
    """Função que executa os testes automaticamente, avalia os resultados, e atualiza a UI."""
    window['STATUS'].update('Executando testes...')
    time.sleep(1)  # Simula tempo para ligar os dispositivos
    
    # Simula resultados dos testes
    results = simulate_test_results()
    evaluation = evaluate_test_results(results)

    # Atualiza a UI com os resultados simulados e status de PASS/FAIL
    window['ESP_VOLTAGE'].update(f"{results['esp_voltage']} V")
    window['DISPLAY_VOLTAGE'].update(f"{results['display_voltage']} V")
    window['SENSOR_VOLTAGE'].update(f"{results['sensor_voltage']} V")
    window['OXYGEN_LEVEL'].update(f"{results['oxygen_level']} %")
    
    window['ESP_RESULT'].update('PASS' if evaluation['esp_pass'] else 'FAIL', text_color='green' if evaluation['esp_pass'] else 'red')
    window['DISPLAY_RESULT'].update('PASS' if evaluation['display_pass'] else 'FAIL', text_color='green' if evaluation['display_pass'] else 'red')
    window['SENSOR_RESULT'].update('PASS' if evaluation['sensor_pass'] else 'FAIL', text_color='green' if evaluation['sensor_pass'] else 'red')
    window['OXYGEN_RESULT'].update('PASS' if evaluation['oxygen_pass'] else 'FAIL', text_color='green' if evaluation['oxygen_pass'] else 'red')
    
    overall_status = 'PASS' if evaluation['overall_pass'] else 'FAIL'
    window['STATUS'].update(f'{overall_status}.', text_color='green' if evaluation['overall_pass'] else 'red')

def main():
    # Aplicando um tema escuro
    sg.theme('DarkBlue17')

    # Layout da interface
    layout = [
        [sg.Text('Porta Serial', size=(12, 1)), sg.InputText('COM3', key='PORT', size=(10, 1)), sg.Button('Conectar', size=(10, 1))],
        [sg.Text('Status:', size=(40, 1), key='STATUS')],
        [sg.Button('Iniciar FCT', size=(25, 1))],
        [sg.Frame('Resultados dos Testes', layout=[
            [sg.Text('Tensão no Microcontrolador:', size=(20, 1)), sg.Text('', size=(15, 1), key='ESP_VOLTAGE'), sg.Text('', size=(10, 1), key='ESP_RESULT')],
            [sg.Text('Tensão Display:', size=(20, 1)), sg.Text('', size=(15, 1), key='DISPLAY_VOLTAGE'), sg.Text('', size=(10, 1), key='DISPLAY_RESULT')],
            [sg.Text('Tensão Sensor:', size=(20, 1)), sg.Text('', size=(15, 1), key='SENSOR_VOLTAGE'), sg.Text('', size=(10, 1), key='SENSOR_RESULT')],
            [sg.Text('Nível de Oxigênio:', size=(20, 1)), sg.Text('', size=(15, 1), key='OXYGEN_LEVEL'), sg.Text('', size=(10, 1), key='OXYGEN_RESULT')]
        ], title_color='orange')],
        [sg.Button('Sair', size=(10, 1))]
    ]

    # Criando a janela
    window = sg.Window('Teste de Oximetro', layout, element_justification='center')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED or event == 'Sair':
            break

        if event == 'Conectar':
            window['STATUS'].update('Tentando conectar...')
            time.sleep(1)  # Simula tempo de conexão
            window['STATUS'].update('Conectado com sucesso.', text_color='green')

        if event == 'Iniciar FCT':
            run_tests(window)

    window.close()

if __name__ == "__main__":
    main()