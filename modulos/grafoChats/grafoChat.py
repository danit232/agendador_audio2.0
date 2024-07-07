from openai import OpenAI
import json
import modulos.idActual as idActual

grafoChats = {}
class grafoChat:
    def __init__(self, id, available_functions, lista_de_tools, lista_de_mensajes, prompt):
        global grafoChats 
        self.id = id
        self.available_functions = available_functions
        self.lista_de_tools = lista_de_tools
        self.lista_de_mensajes = lista_de_mensajes
        self.prompt = prompt
        grafoChats[id] = self
        

    def update_lista_de_mensajes(self):
        lista_de_mensajes = idActual.global_msgs
        lista_de_mensajes_filtrada = []

        validRoles = ["system", "user", "assistant"]
        for mensaje in lista_de_mensajes:
            # Acceder a los valores de cada clave en el diccionario
            
            try:
                if mensaje["role"] in validRoles:
                    lista_de_mensajes_filtrada.append(mensaje)
            except:
                pass
        #self.lista_de_mensajes = lista_de_mensajes_filtrada
        self.lista_de_mensajes = lista_de_mensajes_filtrada
        self.lista_de_mensajes[0] = {"role":"system", "content":self.prompt}


        

    def run_conversation(self):
    # Step 1: send the conversation and available functions to the model
        if idActual.global_id != self.id:
            print(f"DISONANCIA entre {idActual.global_id} y {self.id}")
            grafoChats[idActual.global_id].update_lista_de_mensajes()
            return grafoChats[idActual.global_id].run_conversation()
        
        else:
            client = OpenAI()  # Use your OpenAI API key
            
            print(f"En el BOT {self.id}")
            
            self.update_lista_de_mensajes()
            messages = self.lista_de_mensajes
            #print(messages)
            tools = self.lista_de_tools
            response = client.chat.completions.create(
                model="gpt-3.5-turbo-0125",
                messages=messages,
                tools=tools,
                tool_choice= "auto",  # auto is default, but we'll be explicit
            )
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            # Step 2: check if the model wanted to call a function
            if tool_calls:
                # Step 3: call the function
                # Note: the JSON response may not always be valid; be sure to handle errors
                # only one function in this example, but you can have multiple
                messages.append(response_message)  # extend conversation with assistant's reply
                # Step 4: send the info for each function call and function response to the model
                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_to_call = self.available_functions[function_name]
                    function_args = json.loads(tool_call.function.arguments)
                    lista_de_parametros = list(function_args.keys())
                    primer_parametro = lista_de_parametros[0]
                    function_response = function_to_call(
                        function_args.get(primer_parametro)
                    )
                    print(function_response)
                    messages.append(
                        {
                            "tool_call_id": tool_call.id,
                            "role": "tool",
                            "name": function_name,
                            "content": function_response,
                        }
                    )  # extend conversation with function response
                second_response = client.chat.completions.create(
                    model="gpt-3.5-turbo-0125",
                    messages=messages,
                )  # get a new response from the model where it can see the function response
                if idActual.global_id != self.id:
                    return grafoChats[idActual.global_id].run_conversation()    
                else:    
                    return second_response.choices[0].message.content #+ " acabo de anotar tu " + primer_parametro +  " en una variable: " + function_response
            return response_message.content


