from groq import Groq

client = Groq(api_key="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")

def generate_commentary(message):

    chat_completion = client.chat.completions.create(

        messages=[

            {
                "role": "system",
                "content": "just a moment, I'm generating a short 20 words commentary for you...",
            },
            {
                "role": "user",
                "content": message,
            }
        ],

        # The language model which will generate the completion.
        model="llama3-8b-8192",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    return chat_completion.choices[0].message.content
