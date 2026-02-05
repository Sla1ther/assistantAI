from google import genai
import os
API_KEY = os.getenv("API_KEY")
class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.current_mode = "default"
        self.system_instructions = {}
        self.loadfromFile()
        
    def loadfromFile(self):
        
        instructions_dir = "instructions"
       
        if os.path.exists(instructions_dir):
            for filename in os.listdir(instructions_dir):
                if filename.endswith(".txt"):
                    mode_name = filename[:-4]
                    filepath = os.path.join(instructions_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            self.system_instructions[mode_name] = f.read()
                    except:
                        pass 

        if not self.system_instructions:
         
            pass
    def setMode(self, mode: str):
        
        if mode in self.system_instructions:
            self.current_mode = mode
            return True

        self.current_mode = mode
        return False
   
    def getAvailableModes(self):
        
        return list(self.system_instructions.keys())
    
    def ask(self, prompt):
        try:
            config = {
                "system_instruction": self.system_instructions[self.current_mode],
                
            }
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config=config
                
            )
            if response.text:
                return response.text
            return "No response text received."
        except Exception as e:
            if '429' in str(e):
                return "Rate limit exceeded. Please try again later."
            return f"API error: {str(e)}"
    
    