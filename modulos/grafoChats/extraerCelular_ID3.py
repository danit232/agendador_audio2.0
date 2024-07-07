import modulos.idActual as idActual
import modulos.dataBase.controller as controller
from modulos.dataBase.data_storage import data_storage_instance
from modulos.grafoChats.grafoChat import *

def extraerCelular(celular):
    """Extrae el número celular y lo coloca en el formato json estandar"""
    datos_cliente = {"celular": celular}
    data_storage_instance.add_data('celular', celular)


    if controller.verificarExistencia(json.dumps(datos_cliente)):
        print("El usuario ya existe en la base de datos")
        pass
    else:
        print("No en la base de datos")
        if 'celular' in data_storage_instance.get_data() and 'cedula' in data_storage_instance.get_data() and 'fecha_hora' in data_storage_instance.get_data():
            datos_cliente_completo = data_storage_instance.get_data()
            controller.registrarEntrada(json.dumps(datos_cliente_completo))
            data_storage_instance.clear_data()
        print("Usuario registrado en la base de datos")
        idActual.global_id = 4
    

    return json.dumps({"celular": celular})

def getGrafoChatID3():
    lista_de_tools = [
        {
            
            "type": "function",
            "function": {
                "name": "extraerCelular",
                "description": "Después de que al usuario se le pregunte cual es su número celular y que este responda, se pasa su número celular para que se lo reserve",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "celular": {
                            "type": "string",
                            "description": "Número celular del usuario"
                        },
                    },
                    "required": ["celular"]
                }
            }
        }
        ]

    available_functions = {
                "extraerCelular":extraerCelular
            }

    prompt = """Eres un experto en el agendamiento de citas, ahora tu único trabajo es preguntarle al usuario cual es su número celular. Bajo ninguna otra condición harás cualquier otra acción, considera que puede que recibas una conversación de antemano, evalúa esta conversación y únicamente enfócate en obtener el número de celular del usuario."""

    return grafoChat(3, available_functions, lista_de_tools, None, prompt)