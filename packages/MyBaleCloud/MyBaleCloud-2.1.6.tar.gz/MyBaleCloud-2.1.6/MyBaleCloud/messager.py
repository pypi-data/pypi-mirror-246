class Messenger:
    def __init__(self, result) -> None:
        self.results = result
        
    @property
    def text(self):
        try:
            return self.results['result'][-1]['message']['text']
        except:
            return ""
    
    @property
    def status(self):
        try:
            return self.results['ok']
        except:
            return ""
    
    @property
    def result(self):
        try:
            return self.results['result'][-1]
        except:
            return ""

    @property
    def message(self):
        try:
            return self.results['result'][-1]['message']
        except:
            return ""
    
    @property
    def message_id(self):
        try:
            return self.message['message_id']
        except:
            return ""
    
    @property
    def from_side(self):
        try:
            return self.message['from']
        except:
            return ""
    
    @property
    def from_id(self):
        try:
            return self.from_side['id']
        except:
            return ""
    
    @property
    def from_isbot(self):
        try:
            return self.from_side['is_bot']
        except:
            return ""
        
    @property
    def from_firstname(self):
        try:
            return self.from_side['first_name']
        except:
            return ""
    
    @property 
    def from_lastname(self):
        try:
            return self.from_side['last_name']
        except:
            return ""
    
    @property
    def date(self):
        try:
            return self.message['date']
        except:
            return ""
    
    @property
    def chat_side(self):
        try:
            return self.message['chat']
        except:
            return ""
    
    @property
    def chat_id(self):
        try:
            return self.chat_side['id']
        except:
            return ""
    
    @property
    def chat_type(self):
        try:
            return self.chat_side['type']
        except:
            return ""
    
    @property
    def chat_firstname(self):
        if self.chat_type == 'private':
            try:
                return self.chat_side['first_name']
            except:
                return ""
        else:
            try:
                return False
            except:
                return ""
    
    @property
    def chat_title(self):
        if self.chat_type == 'group':
            try:
                return self.chat_side['title']
            except:
                return ""
        else:
            try:
                return False
            except:
                return ""
    
    @property
    def reply_to_message(self):
        try:
            return self.message['reply_to_message']
        except:
            return None
    
    @property
    def reply_to_message_id(self):
        try:
            return self.message['reply_to_message']['message_id']
        except:
            return None
        
    @property
    def reply_to_message_date(self):
        try:
            return self.message['reply_to_message']['date']
        except:
            return None
    
    @property    
    def reply_to_message_chat(self):
        try:
            return self.message['reply_to_message']['chat']
        except:
            return None
        
    @property
    def reply_to_message_chat_id(self):
        try:
            return self.message['reply_to_message']['chat']['id']
        except:
            return None
    
    @property    
    def reply_to_message_chat_type(self):
        try:
            return self.message['reply_to_message']['chat']['type']
        
        except:
            return None
        
    @property
    def reply_to_message_chat_name(self):
        if self.message['reply_to_message']['chat']['first_name']:
            return self.message['reply_to_message']['chat']['first_name']
            
        elif self.message['reply_to_message']['chat']['title']:
            return self.message['reply_to_message']['chat']['title']
        
    @property
    def reply_to_message_chat_username(self):
        if self.message['reply_to_message']['chat']['username']:
            return self.message['reply_to_message']['chat']['username']
        
        else:
            return None
        
    @property
    def reply_to_message_text(self):
        try:
            return self.message['reply_to_message']['text']
            
        except:
            return None
            
