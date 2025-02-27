import torch
from transformers import BertModel, BertTokenizer
import logging


class EmbeddingProcessor:
    def __init__(self, model_name: str = 'bert-base-uncased'):
        """
        Initializes the EmbeddingProcessor with a specified transformer model.
        """
        self.model, self.tokenizer = self.load_model(model_name)

    def load_model(self, model_name: str):
        """
        Loads the specified model and tokenizer from the HuggingFace Transformers library.
        """
        try:
            tokenizer = BertTokenizer.from_pretrained(model_name)
            model = BertModel.from_pretrained(model_name)
            logging.info(f"Model '{model_name}' and tokenizer loaded successfully.")
            return model, tokenizer
        except Exception as e:
            logging.error(f"Error loading model {model_name}: {e}")
            raise ValueError(f"Unable to load model {model_name}")

    def encode_text(self, text: str):
        """
        Encodes the provided text into embedding using the loaded model and tokenizer.
        """
        if not isinstance(text, str) or len(text.strip()) == 0:
            logging.error("The input text is either not a string or is empty.")
            raise ValueError("Input must be a non-empty string.")

        try:
            # Tokenize input text
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
            # Get the output embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Use the [CLS] token embedding as the sentence embedding
            embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
            logging.info("Text successfully encoded to embedding.")
            return embedding
        except Exception as e:
            logging.error(f"Error encoding text to embedding: {e}")
            raise ValueError(f"Error encoding text to embedding: {e}")

    def batch_encode(self, texts: list):
        """
        Encodes a list of texts into embeddings.
        """
        if not isinstance(texts, list) or len(texts) == 0:
            logging.error("The input must be a non-empty list of strings.")
            raise ValueError("Input must be a non-empty list of strings.")

        if not all(isinstance(text, str) for text in texts):
            logging.error("All items in the list must be strings.")
            raise ValueError("All items in the list must be strings.")

        try:
            # Tokenize input texts
            inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True)
            # Get the output embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
            # Use the [CLS] token embedding as the sentence embedding
            embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            logging.info(f"Successfully encoded {len(texts)} texts to embeddings.")
            return embeddings
        except Exception as e:
            logging.error(f"Error encoding batch of texts to embeddings: {e}")
            raise ValueError(f"Error encoding batch of texts to embeddings: {e}")

    @staticmethod
    def save_embeddings(embeddings, save_path: str):
        """
        Saves the embeddings to a file.
        """
        try:
            with open(save_path, 'wb') as f:
                import pickle
                pickle.dump(embeddings, f)
            logging.info(f"Embeddings saved to {save_path}.")
        except Exception as e:
            logging.error(f"Error saving embeddings to {save_path}: {e}")
            raise ValueError(f"Error saving embeddings to {save_path}")


# Example Usage:

# Initialize the EmbeddingProcessor with a specific model
# embedding_processor = EmbeddingProcessor(model_name='bert-base-uncased')

# Encode a single string
# text = "这是一个示例文本，用于生成embedding。"
# embedding = embedding_processor.encode_text(text)
# print("Single embedding:", embedding)

# Encode a list of texts
# texts = ["这是第一段文本", "这是第二段文本", "这是第三段文本"]
# embeddings = embedding_processor.batch_encode(texts)
# print("Batch embeddings:", embeddings)

# Save embeddings to a file
# embedding_processor.save_embeddings(embeddings, "embeddings.pkl")
