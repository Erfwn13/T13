from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

class DeepConversationalModel:
    def __init__(self, model_name="gpt2", device="cpu"):
        """
        بارگذاری مدل fine-tuned GPT2 (یا مدل پایه) و توکنایزر از دایرکتوری مشخص‌شده.
        """
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name)
        self.model = GPT2LMHeadModel.from_pretrained(model_name)
        self.device = device
        self.model.to(self.device)
        
    def generate_response(self, prompt, max_length=100, temperature=1.0, top_k=50, top_p=0.95):
        try:
            inputs = self.tokenizer.encode(prompt, return_tensors="pt").to(self.device)
            with torch.no_grad():
                outputs = self.model.generate(
                    inputs,
                    max_length=max_length,
                    do_sample=True,
                    temperature=temperature,
                    top_k=top_k,
                    top_p=top_p
                )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return response
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == "__main__":
    model = DeepConversationalModel(device="cuda" if torch.cuda.is_available() else "cpu")
    prompt = "گفتگوی خودکار: جلسه یادگیری جدید"
    print("پاسخ مدل:", model.generate_response(prompt, max_length=150))