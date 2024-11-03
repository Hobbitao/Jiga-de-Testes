import serial
import time
import PySimpleGUI as sg

# Configuração da porta serial (substitua pela sua porta COM)
ser = serial.Serial('COM6', 115200, timeout=1)

# Função para enviar comando de início de teste e receber resultados
def start_tests():
    ser.flushInput()  # Limpa o buffer de entrada
    ser.write(b'START_TEST\n')  # Envia comando para iniciar testes
    time.sleep(1)  # Pausa para ESP processar os testes

    results = {}

    try:
        # Verifica se há dados disponíveis na porta serial
        if ser.in_waiting > 0:
            # Recebe as respostas da serial
            mcu_status = ser.readline().decode('utf-8', errors='ignore').strip()
            display_status = ser.readline().decode('utf-8', errors='ignore').strip()
            sensor_status = ser.readline().decode('utf-8', errors='ignore').strip()
            oxygen_level = ser.readline().decode('utf-8', errors='ignore').strip()

            results = {
                'mcu': mcu_status,
                'display': display_status,
                'sensor': sensor_status,
                'oxygen': oxygen_level
            }
        else:
            results = {
                'mcu': 'No response',
                'display': 'No response',
                'sensor': 'No response',
                'oxygen': 'No response'
            }
    except Exception as e:
        print(f"Erro ao ler a serial: {e}")
        results = {
            'mcu': 'Erro',
            'display': 'Erro',
            'sensor': 'Erro',
            'oxygen': 'Erro'
        }

    return results

# Função para verificar se o teste passou ou falhou
# Função para verificar se o teste passou ou falhou
# Função para verificar se o teste passou ou falhou
def check_pass_fail(results):
    # Log para depuração, mostrando exatamente o que está sendo recebido
    print("DEBUG - Resultados Recebidos:")
    print(f"MCU Status: '{results['mcu']}'")
    print(f"Display Status: '{results['display']}'")
    print(f"Sensor Status: '{results['sensor']}'")
    print(f"Nível de Oxigênio: '{results['oxygen']}'")

    try:
        # Remover espaços em branco antes e depois e garantir letras maiúsculas
        mcu_status = results['mcu'].strip().upper()
        display_status = results['display'].strip().upper()
        sensor_status = results['sensor'].strip().upper()

        # Captura e conversão do nível de oxigênio, removendo espaços
        oxygen_value = float(results['oxygen'].split(":")[1].strip()) if ':' in results['oxygen'] else float(results['oxygen'].strip())

        # Log para depuração do valor de oxigênio
        print(f"Valor de Oxigênio (convertido): {oxygen_value}")

    except ValueError:
        # Se ocorrer erro ao converter o valor de oxigênio, atribuímos 0
        oxygen_value = 0
        print("Erro ao converter o valor de oxigênio")

    # Verificar as condições
    if (mcu_status == 'MCU: PASS' and 
        display_status == 'DISPLAY: PASS' and 
        sensor_status == 'SENSOR: PASS' and 
        oxygen_value >= 88.5):
        return 'pass'
    else:
        return 'fail'

# Configuração do tema escuro da interface
sg.theme('DarkGrey13')

# Layout da interface com log de teste
layout = [
    [sg.Text('Jiga De Testes', font=('Helvetica', 20), justification='center', pad=(0, 20))],
    [
        sg.Column([
            [sg.Text('Microcontrolador:', size=(20, 1), font=('Helvetica', 16)), sg.Text('', key='mcu_status', size=(15, 1), font=('Helvetica', 16))],
            [sg.Text('Display:', size=(20, 1), font=('Helvetica', 16)), sg.Text('', key='display_status', size=(15, 1), font=('Helvetica', 16))],
            [sg.Text('Sensor de Oxigênio:', size=(20, 1), font=('Helvetica', 16)), sg.Text('', key='sensor_status', size=(15, 1), font=('Helvetica', 16))],
            [sg.Text('Nível de Oxigênio (%):', size=(20, 1), font=('Helvetica', 16)), sg.Text('', key='oxygen_level', size=(15, 1), font=('Helvetica', 16))],
            [sg.Button('Iniciar Testes', size=(20, 2), font=('Helvetica', 14)), sg.Button('Sair', size=(20, 2), font=('Helvetica', 14))]
        ]),
        sg.VerticalSeparator(),
        sg.Column([
            [sg.Text('Log de Teste:', font=('Helvetica', 16))],
            [sg.Multiline(size=(40, 20), key='log_output', font=('Helvetica', 12), disabled=True)],
            [sg.Text('', key='pass_fail_message', font=('Helvetica', 16), size=(20, 1))]
        ])
    ]
]

# Cria a janela da interface com tamanho maior
window = sg.Window('Jiga de Teste de Oxímetro', layout, size=(1000, 600), element_justification='center')

# Loop de eventos da interface
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    if event == 'Iniciar Testes':
        # Envia o comando de teste e recebe os resultados
        results = start_tests()

        # Atualiza a interface com os resultados
        window['mcu_status'].update(results['mcu'])
        window['display_status'].update(results['display'])
        window['sensor_status'].update(results['sensor'])
        window['oxygen_level'].update(results['oxygen'].split(":")[1] + "%" if ':' in results['oxygen'] else results['oxygen'])

        # Adiciona os resultados ao log
        log_message = f"MCU Status: {results['mcu']}\n" \
                      f"Display Status: {results['display']}\n" \
                      f"Sensor Status: {results['sensor']}\n" \
                      f"Nível de Oxigênio: {results['oxygen']}\n" \
                      "-----------------------------------\n"
        window['log_output'].update(log_message, append=True)

        # Verifica se passou ou falhou
        test_result = check_pass_fail(results)

        # Exibe mensagem de Pass ou Fail com cor
        if test_result == 'pass':
            window['pass_fail_message'].update('PASS', text_color='green', font=('Helvetica', 16, 'bold'))
        else:
            window['pass_fail_message'].update('FAIL', text_color='red', font=('Helvetica', 16, 'bold'))

# Fecha a porta serial e a janela da interface
ser.close()
window.close()
