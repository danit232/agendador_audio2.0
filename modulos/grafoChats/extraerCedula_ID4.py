import modulos.idActual as idActual
import modulos.dataBase.controller as controller
from modulos.grafoChats.grafoChat import *
from modulos.dataBase.data_storage import data_storage_instance

def extraerCedula(cedula):
    """Extrae el número de cédula y lo coloca en el almacenamiento temporal"""
    data_storage_instance.add_data('cedula', cedula)

    if controller.verificarExistencia(json.dumps({"cedula": cedula})):
        print("El usuario ya existe en la base de datos")
    else:
        print("No en la base de datos")
        if 'nombreCompleto' in data_storage_instance.get_data() and 'celular' in data_storage_instance.get_data() and 'fecha_hora' in data_storage_instance.get_data():
            datos_cliente_completo = data_storage_instance.get_data()
            controller.registrarEntrada(json.dumps(datos_cliente_completo))
            data_storage_instance.clear_data()
        idActual.global_id = 5

    return json.dumps({"cedula": cedula})

def getGrafoChatID4():
    lista_de_tools = [
        {
            "type": "function",
            "function": {
                "name": "extraerCedula",
                "description": "Después de que al usuario se le pregunte cual es su número de cédula y que este responda, se pasa su número de cédula para que se lo reserve",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cedula": {
                            "type": "integer",
                            "description": "Número de cédula del usuario"
                        },
                    },
                    "required": ["cedula"]
                }
            }
        }
    ]

    available_functions = {
                "extraerCedula": extraerCedula
            }

    prompt = """Eres un experto en el agendamiento de citas, ahora tu único trabajo es preguntarle al usuario cual es su número de cédula. Bajo ninguna otra condición harás cualquier otra acción, considera que puede que recibas una conversación de antemano, evalúa esta conversación y únicamente enfócate en obtener el número de cédula del usuario."""

    return grafoChat(4, available_functions, lista_de_tools, None, prompt)
