from volcengine.maas.text_privatization import ClsPrivConf
from volcengine.maas.text_privatization import make_privatizer
from volcengine.maas.text_privatization import get_bottom_model



if __name__ == '__main__':
    # Prepare your tokenizer and embedding model. You can use the `get_bottom_model` method to get the
    # tokenizer and embedding module of an open source pre-trained model from hugging face.
    your_tokenizer, your_embedding_model = get_bottom_model(model_id="MODEL_ID")
    # Initialize a text privatizer instance
    text_privatizer = make_privatizer(task_type="classification", priv_conf=ClsPrivConf(priv_level="3"))
    # Load tokenizer and embedding model
    text_privatizer.load_tokenizer_embedding(tokenizer=your_tokenizer, embedding_model=your_embedding_model)
    # Given the training data path, use the `fit` method to perform text privatization.
    text_privatizer.fit(train_path="PATH/TO/DATA.jsonl")
    # Save
    text_privatizer.save(out_dir="PATH/TO/SAVE")





