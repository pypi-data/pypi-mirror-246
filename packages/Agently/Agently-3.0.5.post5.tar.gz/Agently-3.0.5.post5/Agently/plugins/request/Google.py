from .utils import RequestABC
import google.generativeai as genai

class Google(RequestABC):
    def __init__(self, request):
        self.request = request
        self.model_name = "Google"
        self.model_settings = RuntimeCtxNamespace(f"model.{ self.model_name }", self.request.settings)
        
    def construct_request_messages(self):
        return 

    def generate_request_data(self):
        return

    def request_model(self, request_data: dict):
        return

    def broadcast_response(self, response_generator):
        return

    def export(self):
        return {
            "generate_request_data": self.generate_request_data,
            "request_model": self.request_model,
            "broadcast_response": self.broadcast_response,
        }

def export():
    return ("Google", Google)