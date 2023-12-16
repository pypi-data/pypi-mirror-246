import os
import time
import json
from dotenv import load_dotenv

load_dotenv()

class Assistant:
    def __init__(self, config, name, instructions, model, assistant_id=None, thread_id=None, event_listener=None):
        try:
            from openai import OpenAI
        except ImportError:
            OpenAI = None

        if OpenAI is None:
            raise ImportError("The OpenAI library is required to use this functionality. Please install it with `pip install Your-Library[openai]`.")
        self.config = config
        self.name = name
        self.instructions = instructions
        self.model = model
        self.event_listener = event_listener
        self.assistant_id = assistant_id
        self.thread_id = thread_id
        self.openai_client = OpenAI()
        self.assistant, self.thread = self.create_assistant_and_thread()

    # Create an OpenAI assistant and a thread for interactions
    def create_assistant_and_thread(self):
        # Extract tools from the Alpha Vantage config
        tools = self.config.generate_tools_representation()
        desc_string = ""
        if self.config.model_description is not None and self.config.model_description != "none":
            desc_string =  " Tool information below\n---------------\n"+self.config.model_description
        # Initialize the OpenAI assistant
        if self.assistant_id is not None:
            assistant = self.openai_client.beta.assistants.retrieve(self.assistant_id)
            if self.thread_id is not None:
                thread = self.openai_client.beta.threads.retrieve(self.thread_id)
                runs = self.openai_client.beta.threads.runs.list(self.thread_id)
                if len(runs.data) > 0:
                    latest_run = runs.data[0]
                    if(latest_run.status == "in_progress" or latest_run.status == "queued" or latest_run.status == "requires_action"):
                        run = self.openai_client.beta.threads.runs.cancel(thread_id=self.thread_id, run_id = latest_run.id)
                        print('cancelled run')
            else:
                thread = self.openai_client.beta.threads.create()
        else:
            assistant = self.openai_client.beta.assistants.create(
                name=self.name,
                instructions=self.instructions+desc_string,
                model=self.model,
                tools=tools,
            )
            self.assistant_id = assistant.id
            thread = self.openai_client.beta.threads.create()
            self.thread_id = thread.id
            #print("Thread ID: save this for persistence: "+thread.id)

        # Create a thread for the assistant
        return assistant, thread


    def get_assistant_response(self,message):
        message = self.openai_client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message
        )
        run = self.openai_client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            )
        print("Waiting for response")
        print(run.id)
        completed = False
        while not completed:
            run_ = self.openai_client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
            if run_.status == "completed":
                break
            elif run_.status == "failed":
                print("Run failed")
                break
            elif run_.status == "cancelled":
                print("Run cancelled")
                break
            elif run_.status == "requires_action":
                print("Run requires action")
                tool_calls = run_.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                for tool_call in tool_calls:
                    #print(tool_call)
                    if self.event_listener is not None:
                        self.event_listener(tool_call)
                    if tool_call.type == "function":
                        result = self.execute_function(tool_call.function.name, tool_call.function.arguments)
                        output = {
                            "tool_call_id": tool_call.id,
                            "output": json.dumps(result)
                        }
                        #print(output)
                        #put output to event listener if there is one
                        if self.event_listener is not None:
                            self.event_listener(output)
                        tool_outputs.append(output)
                run__ = self.openai_client.beta.threads.runs.submit_tool_outputs(thread_id=self.thread.id, run_id=run.id, tool_outputs=tool_outputs)
            time.sleep(5)
        run_ = self.openai_client.beta.threads.runs.retrieve(thread_id=self.thread.id, run_id=run.id)
        messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread.id)
        print(messages.data[0].content[0].text.value)
        return messages.data[0].content[0].text.value
    def get_entire_conversation(self):
        messages = self.openai_client.beta.threads.messages.list(thread_id=self.thread.id)
        return messages.data
    def execute_function(self,function_name, arguments):
        """Execute a function and return the result."""
        #example of function_name: "alpha_vantage/query"
        #config.make_api_call_by_operation_id("genericQuery", params={"function": "TIME_SERIES_DAILY", "symbol": "BTC", "market": "USD"}
        #config.make_api_call_by_path("/query", "GET", params={"function": "TIME_SERIES_DAILY", "symbol": "BTC", "market": "USD"})
        #actual implementation of the function
        #turn arguments into dictionary
        arguments = json.loads(arguments)
        try:
            request = self.config.make_api_call_by_operation_id(function_name, params=arguments)
            return request.json()
        except Exception as e:
            print(e)
            try:
                #split the function name into path and method by - eg query-GET
                split = function_name.split("-")
                method = split[1]
                path = split[0]
                request = self.config.make_api_call_by_path('/'+path, method.upper(), params=arguments)
                print(request.json())
                return request.json()
            except Exception as e:
                print(e)
                #debug stack trace
                import traceback
                traceback.print_exc()
                try:
                    request = self.config.make_api_call_by_path(path, method.upper(), params=arguments)
                    return request.json()
                except Exception as e:
                    print(e)
                    return "Error"
