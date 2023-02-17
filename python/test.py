import openai
import wandb
import whisper

## This needs to be deleted from the code before running as the key is private
openai.api_key = "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"

# initialize wandb
run = wandb.init(project='GPTeach')
prediction_table = wandb.Table(columns=["prompt", "completion"])


## Prompt given here
gpt_prompt = "Do you know the fitnessgram pacer test?"


# Generate response from GPT-3 
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=gpt_prompt,
    temperature=0.4,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0.0,
    presence_penalty=0.0,
    )

# Print the response
print(response["choices"][0]["text"])
prediction_table.add_data(gpt_prompt, response["choices"][0]["text"])

# Log the response to wandb
wandb.log({"predictions": prediction_table})
wandb.finish()

