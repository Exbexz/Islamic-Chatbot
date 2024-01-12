
from transformers import AutoTokenizer,AutoModel,pipeline


def vectorize(sentence,model_path_index):
    #sentence = input("Your sentence: ")
    if model_path_index == 1:
        #path = "Vectorizer\google-canine-c"
        path = "https://github.com/Exbexz/Islamic-Chatbot/tree/c59d607538d69bb0d27101b1e8da71d574610934/Vectorizer/google-canine-c"

    elif model_path_index == 2:
        path = "Vectorizer\malaysian-debartav-base"

    elif model_path_index == 3:   
        path = "Vectorizer\multilingual-e5-large"

    elif model_path_index == 4:  
        import malaya
        model = malaya.transformer.load(model='bert')
        sentence = [sentence]
        vector = model.vectorize(sentence)
   
        return vector[0]
    
    elif model_path_index == 5:
        from openai import OpenAI
        #from dotenv import load_dotenv
        import os

        #load_dotenv()
 
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI()

        vector=client.embeddings.create(input = [sentence], model='text-embedding-ada-002')
        return vector.data[0].embedding

    else:
        print('''Please provide a proper index for the model
              \n1 google-canine-c 
              \n2 malaysian-debartav3-base
              \n3 multilingual-e5-large
              \n4 malaya-bert-model
              \n5 openAI text-embedding-ada-002 model''')
        
        return ModuleNotFoundError
    
    model = AutoModel.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)

    pipe = pipeline(task="feature-extraction",model=model,tokenizer=tokenizer)

    vector = pipe(sentence)
    return vector[0][0]