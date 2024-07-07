import modulos.idActual as idActual
import modulos.dataBase.controller as controller
from modulos.dataBase.data_storage import data_storage_instance
from modulos.grafoChats.grafoChat import *

def extraerNombreCompleto(nombreCompleto):
    """Extrae el nombre completo y lo coloca en el formato json estandar"""
    datos_cliente = {"nombreCompleto": nombreCompleto}
    data_storage_instance.add_data('nombreCompleto', nombreCompleto)

    if controller.verificarExistencia(json.dumps(datos_cliente)):
        print("El usuario ya existe en la base de datos")
        idActual.global_id = 3
        pass
    else:
        print("No en la base de datos")
        if 'celular' in data_storage_instance.get_data() and 'cedula' in data_storage_instance.get_data() and 'fecha_hora' in data_storage_instance.get_data():
            datos_cliente_completo = data_storage_instance.get_data()
            controller.registrarEntrada(json.dumps(datos_cliente_completo))
            print("Usuario registrado en la base de datos")
            data_storage_instance.clear_data()
        idActual.global_id = 3


    return json.dumps({"nombreCompleto": nombreCompleto})

def getGrafoChatID2():
    lista_de_tools = [
        {
            
            "type": "function",
            "function": {
                "name": "extraerNombreCompleto",
                "description": "Después de que al usuario se le pregunte cual es su nombre completo y que este responda, se pasa su nombre completo para que se lo reserve",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "nombreCompleto": {
                            "type": "string",
                            "description": "Nombre completo del usuario"
                        },
                    },
                    "required": ["nombreCompleto"]
                }
            }
        }
        ]

    available_functions = {
                "extraerNombreCompleto":extraerNombreCompleto
            }

    prompt = """Eres un experto en el agendamiento de citas, ahora tu único trabajo es preguntarle al usuario cual es su nombre completo. Bajo ninguna otra condición harás cualquier otra acción, considera que puede que recibas una conversación de antemano, evalúa esta conversación y únicamente enfócate en obtener el nombre completo del usuario."""

    return grafoChat(2, available_functions, lista_de_tools, None, prompt)