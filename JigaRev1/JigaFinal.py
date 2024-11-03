import serial
import PySimpleGUI as sg
import json

# Configuração da porta serial (ajuste conforme necessário)
serial_port = 'COM6'  # Porta COM ou '/dev/ttyUSB0' no Linux
baud_rate = 115200

# Inicializar a conexão serial
ser = serial.Serial(serial_port, baud_rate, timeout=1)

# Layout da interface gráfica
layout = [
    [sg.Text('Oxímetro e Jiga - Status do Teste', size=(30, 1), font=("Helvetica", 25))],
    [sg.Text('Status:', size=(15, 1)), sg.Text('', key='STATUS')],
    [sg.Text('BPM:', size=(15, 1)), sg.Text('', key='BPM')],
    [sg.Text('Média BPM:', size=(15, 1)), sg.Text('', key='AVG_BPM')],
    [sg.Text('Valor IR:', size=(15, 1)), sg.Text('', key='IR')],
    [sg.Output(size=(60, 10), key='Output')],
    [sg.Button('Sair')]
]

# Inicializar a janela da interface gráfica
window = sg.Window('Interface de Jiga e Oxímetro', layout, finalize=True)

def update_gui(data):
    """Função para atualizar a interface gráfica com os dados recebidos do JSON"""
    try:
        window['STATUS'].update(data['status'])
        window['BPM'].update(data['bpm'])
        window['AVG_BPM'].update(data['avg_bpm'])
        window['IR'].update(data['ir_value'])
    except KeyError as e:
        print(f"Erro ao processar dados: {e}")

# Loop principal da interface gráfica
while True:
    event, values = window.read(timeout=100)

    # Verificar se o botão 'Sair' foi pressionado
    if event == sg.WIN_CLOSED or event == 'Sair':
        break

    # Ler dados da serial
    if ser.in_waiting > 0:
        json_str = ser.readline().decode('utf-8').strip()
        if json_str:
            try:
                # Desserializar o JSON recebido
                data = json.loads(json_str)
                update_gui(data)
                print(f"Dados recebidos: {data}")
            except json.JSONDecodeError:
                print(f"Erro ao decodificar JSON: {json_str}")

# Encerrar a conexão serial e fechar a janela
ser.close()
window.close()