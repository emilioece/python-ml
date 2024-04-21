from openai import OpenAI
from keys import API_TOKEN

#TODO: Get probability from model and issue.
# def model_feedback():
#   probablity = 0
#   issue = 'brain lesion'
#   return (probablity, issue)

def generate_response(issue:str, confidence:str) -> str:
    confidence = '1'
    issue = 'lesion selar'
    organ_test = 'brain tumor xray'
    # confidence, issue = model_feedback() 
    client = OpenAI(api_key = API_TOKEN)
    user_content = f"Organ status = {confidence}" 
    system_content = f"Please provide the result of your recent {organ_test}. Based on the confidence, {confidence} feedback, give consultation to the patient and explain what {issue} is if present, that is , if {confidence} = 1, however, if {confidence} = 0, explain that no problems were found and reassure good health of the patient. Make the response less than 256 tokens please."

    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {
          "role": "system",
          "content": system_content
        },
        {
          "role": "user",
          "content": user_content     }
      ],
      temperature=0.4,
      max_tokens=256,
      top_p=1
    )
   
    processed_response = response.choices[0].message.content
    return processed_response

if __name__ == '__main__':
    print('meow')