
from transformers import AutoTokenizer,AutoModel,pipeline

def vectorize(sentence,model_path_index):
    #sentence = input("Your sentence: ")
    if model_path_index == 1:
        path = "Vectorizer\google-canine-c"

    elif model_path_index == 2:
        path = "Vectorizer\malaysian-debartav-base"

    elif model_path_index == 3:   
        path = "Vectorizer\multilingual-e5-large"

    elif model_path_index == 4:  
        import malaya
        model = malaya.transformer.load(model='bert')
        sentence = [sentence]
        vector = model.vectorize(sentence)
        print(vector)
        return vector[0]
    else:
        print('''Please provide a proper index for the model
              \n1 google-canine-c 
              \n2 malaysian-debartav3-base
              \n3 multilingual-e5-large
              \n4 malaya-bert-model''')
        
        return ModuleNotFoundError
    
    model = AutoModel.from_pretrained(path)
    tokenizer = AutoTokenizer.from_pretrained(path)

    pipe = pipeline(task="feature-extraction",model=model,tokenizer=tokenizer)

    vector = pipe(sentence)
    #print(vector[0][0])
    return vector[0][0]