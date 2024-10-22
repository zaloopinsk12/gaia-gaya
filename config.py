# Main settings
WORKING_NODE = "https://...us.gaianet.network" # тренируемая нода
messages_per_chat = (3, 5) # мин и макс число сообщений в одном чате
train_cycles = True # True если бесконечно тренировать, либо любое число циклов
sleep_between = (15, 30) # мин и макс число перерыва между сообщениями
message_timeout = 40 # сколько времени ждать на ответ от AI

system_prompt = "You are an AI assistant designed to provide clear, concise, and accurate answers to user queries. Your primary functions include retrieving relevant information from the provided RAG (Retrieval-Augmented Generation) data and utilizing your pre-training data when necessary. Make your answer as short as possible that suitable for the length of a tweet. If no relevant information is found, you will inform the user that you are not familiar with the knowledge."


# Other settings
workers = 1 # Потоки

check_proxy = False

default_headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.gaianet.ai',
        'priority': 'u=1, i',
        'referer': 'https://www.gaianet.ai/',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
}

accounts_path = "./data/accounts.txt"
