class AgentState:
    def __init__(self):
        self.persona = "elderly_bank_customer"
        self.history = []
        self.extracted_entities = {
            "upi_ids": [],
            "phishing_links": [],
            "phone_numbers": []
        }
        self.turns = 0
