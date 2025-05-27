from transformers import (DataCollatorForLanguageModeling, GPT2LMHeadModel,
                          GPT2Tokenizer, TextDataset, Trainer,
                          TrainingArguments)


def fine_tune_model(train_file, model_name="gpt2", output_dir="fine_tuned_model"):
    # بارگذاری توکنایزر و مدل اولیه
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # ایجاد دیتاست از فایل متنی داده‌های مکالمه
    dataset = TextDataset(tokenizer=tokenizer, file_path=train_file, block_size=128)
    data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

    training_args = TrainingArguments(
        output_dir=output_dir,
        overwrite_output_dir=True,
        num_train_epochs=3,
        per_device_train_batch_size=4,
        save_steps=500,
        save_total_limit=2,
        prediction_loss_only=True,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        data_collator=data_collator,
        train_dataset=dataset,
    )

    trainer.train()
    model.save_pretrained(output_dir)
    tokenizer.save_pretrained(output_dir)
    print("Fine-tuning completed. Model saved to:", output_dir)


if __name__ == "__main__":
    # مسیر فایل داده‌های مکالمه را به روز کنید
    fine_tune_model("c:\\Developer\\T13_Project\\data\\conversation_data.txt")
