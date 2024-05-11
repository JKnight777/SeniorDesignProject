# This file is used to train the Gemma 2B model
# This file uses Huggingface, and trains off of local data
# After training is completed, the model is named and saved
import os
import transformers
import torch
import datetime
from datasets import load_dataset
from trl import SFTTrainer
from peft import LoraConfig
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import BitsAndBytesConfig
from datetime import datetime, date

# This is the token for access to the base model off of HuggingFace
os.environ["HF_TOKEN"] = "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"

# Configure the bitsandbytes and set model id here
model_id = "google/gemma-2b"
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# 32 bits of parameters (weights and bias) are convereted to 4 bits
# bnb_4bit_quant_type="nf4" --> 4 bit normal float is a technique used here for quantization
# bnb_4bit_compute_dtype=torch.bfloat16 --> Due to quantization, there is loss of information,
#    to balance that float16 is used for weights related fine tuning

#Get the model and its tokenizer off of the hub
tokenizer = AutoTokenizer.from_pretrained(model_id, token=os.environ['HF_TOKEN'])
model = AutoModelForCausalLM.from_pretrained(model_id,
                                             quantization_config=bnb_config,
                                             device_map={"":0},
                                             token=os.environ['HF_TOKEN'])

# device_map={"":0} is for GPU

# Set up LORA Config
os.environ["WANDB_DISABLED"] = "false"
lora_config = LoraConfig(
    r = 8,
    target_modules = ["q_proj", "o_proj", "k_proj", "v_proj",
                      "gate_proj", "up_proj", "down_proj"],
    task_type = "CAUSAL_LM",
)

# r = 8 rank of LORA, hyper-parameter, u can choose 4,8,16,34,64

from datasets import load_dataset

# Load local dataset to be used for training
data = load_dataset("csv", data_files="Food.csv")

# Map the data for the model
data = data.map(lambda samples: tokenizer(samples["name"]), batched=True)

# Supervised Fine Tuning format
# This is the format the model should learn to emulate when asked questions in this style
def formatting_func(example):
    text = f"Name: {example['name'][0]}\nIndian?: {example['cuisine'][0]}"
    return [text]

data['train']

# Trains the model off of the dataset
trainer = SFTTrainer(
    model=model,
    train_dataset=data["train"],
    args=transformers.TrainingArguments(
        per_device_train_batch_size=1,
        gradient_accumulation_steps=4,
        warmup_steps=2,
        max_steps=1000,
        learning_rate=2e-4,
        fp16=True,
        logging_steps=1,
        output_dir="outputs",
        optim="paged_adamw_8bit"
    ),
    peft_config=lora_config,
    formatting_func=formatting_func,
)

trainer.train()

# Set to GPU
device = "cuda:0" 

# This is the test for the model to take
# It consists of 20 dishes,
#   10 are Indian, 10 are not
#   5 of those 10 Indian recipes are on the dataset
#   5 are new, but still Indian
#   5 of the 10 notIndian recipes are on the dataset
#   5 are new, but still notIndian

model = model.to(device)
dishes = [
    #Indian
    'Oats and Date Cookie', 
    'Quinoa Bath', 
    'Cauliflower Curry With Bell Peppers And Carrots In Spiced Milk Gravy', 
    'Atta Biscuit', 
    'Raw Banana Raita',
    #Not from dataset 
    'Chicken Makhani', 
    'Keema Samosas', 
    'Aloo Gobi',
    'Butter and Garlic Naan',
    'Matar Paneer',

    #Not Indian 
    'Chicken, Mushroom And Broccoli Au Gratin',
    'Chocolate Chip Cookie',
    'Thai Red Curry',
    'Pesto and Tangy Tomato Whirls',
    'Cheesy Spinach Enchilada',
    #Not from dataset
    'Cheese and Pepperoni Pizza',
    'Pork Ramen',
    'Seafood Paella',
    'Feta and Spinach Pierogi',
    'Eggplant Moussaka',
    ]

# Go through each one, have the model try to answer it
for dish in dishes:
    inputs = tokenizer(f"Name: {dish} Recipe\n", return_tensors="pt").to(device)
    outputs = model.generate(**inputs, max_new_tokens=20)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True), end="\n\n")

# Once finished with training, save the model with a timestamp
timestamp = str(date.today())
timestamp += ";" + str(datetime.now().strftime("%H-%M-%S"))
trainer.save_model(f"./Models/Gemma2b;{timestamp}")
print("Model saved to ./Models/Gemma2b;" + timestamp)