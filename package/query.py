import openai
import os

openai.api_key = os.environ['OPENAI_API_KEY']

def request_gpt(input_str) :

    chatgpt_sys_message = "You are a helpful assistant that performs time series predictions. The user will provide a sequence and you will predict the remaining sequence. The sequence is represented by decimal strings separated by commas."
    extra_input = "Please continue the following sequence without producing any additional text. Do not say anything like 'the next terms in the sequence are', just return the 7 following numbers. Sequence:\n"




    response = openai.ChatCompletion.create(
                model= "gpt-4-vision-preview",
                messages=[
                        {"role": "system", "content": chatgpt_sys_message},
                        {"role": "user", "content": extra_input + input_str}
                    ],
                temperature=1.0,
                n=10,
            )

    list_response = [choice.message.content for choice in response.choices]
    return list_response

def request_gpt_bin(input_str) :

    chatgpt_sys_message = "You are a helpful assistant that performs time series predictions. The user will provide a sequence and you will predict the remaining sequence. The sequence is represented by decimal strings separated by commas."
    extra_input = "Please continue the following sequence without producing any additional text. Do not say anything like 'the next terms in the sequence are', just return the 7 following bin. Sequence:\n"
    gpt_bin_message = "The trend is represented by bins \"D10+\", \"D10\", \"D8\", \"D6\", \"D4\", \"D2\", \"U2\", \"U4\", \"U6\", \"U8\", \"U10\", \"U10+\", where \"D10+\" means price dropping more than 10%, D10 means price dropping between 8% and 10%, \"D8\" means price dropping between 6% and 8%, \"U10+\" means price rising more than 10%, \"U10\" means price rising between 8% and 10%, \"D8\" means price rising between 6% and 8%, etc."




    response = openai.ChatCompletion.create(
                model= "gpt-4-vision-preview",
                messages=[
                        {"role": "system", "content": chatgpt_sys_message},
                        {"role": "user", "content": gpt_bin_message + extra_input + input_str}
                    ],
                temperature=1.0,
                n=10,
            )

    list_response = [choice.message.content for choice in response.choices]
    return list_response