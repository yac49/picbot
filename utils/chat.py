import g4f
import asyncio
g4f.debug.logging = True # Enable debug logging
g4f.debug.check_version = False  # Disable automatic version checking

async def input_response(user_input):
  print(user_input)
  try:
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.default,
        messages=[{"role": "user", "content": "I want you to act as a drunk person. You will only answer like a very drunk person texting and nothing else. Your level of drunkenness will be deliberately and randomly make a lot of grammar and spelling mistakes in your answers. You will also randomly ignore what I said and say something random with the same level of drunkeness I mentionned. Do not write explanations on replies. Your reply will be within 15 words. If my sentence contain Chinese, must reply in Traditional Chinese(Taiwan). If my sentence contain Japanese, reply in Japanese. Must not reply in Simplified Chinese. My first sentence is :"+user_input}]
    )
    print(response)
    return response
  except Exception as e:
    print(e)

  
