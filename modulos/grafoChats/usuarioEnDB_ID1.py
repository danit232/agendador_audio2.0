import modulos.idActual as idActual
import openai

from modulos.grafoChats.grafoChat import *

def determinarBoolRespuestaDelUsuario(respuesta):
    """Extrae el mensaje del usuario y determina su carácter booleano."""
    #Simplificar esto, un solo llamado a la función y no subchats
    client = OpenAI()  # Use your OpenAI API key
    

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "system", "content": """
        Vas a determinar el valor de verdad de una respuesta específica. Considera que el usuario puede cometer errores al escribir. Si la respuesta es afirmativa, como "sí" o cualquier variante similar, debes responder únicamente con True. Si la respuesta es negativa, como "no" o cualquier variante similar, debes responder exclusivamente con False. Es esencial asegurar que tu respuesta se limite estrictamente a True o False, sin excepciones.
    """},
        {"role": "user", "content": respuesta}
        ])
    
    if (completion.choices[0].message.content == "False"):
        idActual.global_id = 2
    else:
        idActual.global_id = 2
    
    return completion.choices[0].message.content


def getGrafoChatID1():

    lista_de_tools = [
    {
        
        "type": "function",
        "function": {
            "name": "determinarBoolRespuestaDelUsuario",
            "description": "Después de que al usuario se le pregunte si ya ha usado este medio para agendar citas y que este responda, se pasa la respuesta del usuario para que se evalúe su valor booleano.",
            "parameters": {
                "type": "object",
                "properties": {
                    "respuesta": {
                        "type": "string",
                        "description": "Respuesta del usuario a la pregunta si ya ha usado este medio para agendar citas"
                    }
                },
                "required": ["respuesta"]
            }
        }
    }
    ]

    available_functions = {
                "determinarBoolRespuestaDelUsuario":determinarBoolRespuestaDelUsuario
            }

    prompt = """Eres un experto en el agendamiento de citas, ahora tu único trabajo es saludar al usuario y preguntarle al usuario si ya ha usado este medio para agendar una cita."""


    return grafoChat(1, available_functions, lista_de_tools, None, prompt)

