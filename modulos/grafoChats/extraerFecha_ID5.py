import modulos.idActual as idActual
import modulos.dataBase.controller as controller
from modulos.grafoChats.grafoChat import *
from modulos.dataBase.data_storage import data_storage_instance

def extraerFecha(fecha_hora):
    """Extrae la fecha y hora y lo coloca en el almacenamiento temporal"""
    data_storage_instance.add_data('fecha_hora', fecha_hora)

    if controller.verificarExistencia(json.dumps({"fecha_hora": fecha_hora})):
        print("El usuario ya existe en la base de datos")
    else:
        print("No en la base de datos")
        if 'nombreCompleto' in data_storage_instance.get_data() and 'celular' in data_storage_instance.get_data() and 'cedula' in data_storage_instance.get_data():
            datos_cliente_completo = data_storage_instance.get_data()
            controller.registrarEntrada(json.dumps(datos_cliente_completo))
            data_storage_instance.clear_data()
        #idActual.global_id = 3

    return json.dumps({"fecha_hora": fecha_hora})

def getGrafoChatID5():
    lista_de_tools = [
        {
            "type": "function",
            "function": {
                "name": "extraerFecha",
                "description": "Después de que al usuario se le pregunte la fecha y hora en que desea agendar la cita y que este responda, se pasa su fecha y hora para que lo reserve",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fecha_hora": {
                            "type": "string",
                            "format": "date-time",
                            "description": "Fecha y hora de cita del usuario en formato ISO 8601"
                        },
                    },
                    "required": ["fecha_hora"]
                }
            }
        }
    ]

    available_functions = {
                "extraerFecha": extraerFecha
            }

    prompt = """Eres un experto en el agendamiento de citas, ahora tu único trabajo es preguntarle al usuario la fecha y hora en que desea agendar su cita. Bajo ninguna otra condición harás cualquier otra acción, considera que puede que recibas una conversación de antemano, evalúa esta conversación y únicamente enfócate en obtener la fecha y hora de la cita que desea el usuario."""

    return grafoChat(5, available_functions, lista_de_tools, None, prompt)
