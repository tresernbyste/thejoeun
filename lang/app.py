from flask import Flask, request, render_template
from chat_model import ChatModel
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/english', methods=['GET', 'POST'])
def englishConv():
    answer = None
    conversation = []
    if request.method == 'POST':
        question = request.form['question']

        chat_model = ChatModel()
        chain = chat_model.generate_response()

        answer = chain.invoke({"question": question})
 

        def parse_conversation(text):
            english_conversations = []
            korean_translations = []
            for line in text.split("\n"):
                if line.startswith("영어 회화"):
                    english_conversations.append(line.split(": ", 1)[1])
                elif line.startswith("한글 해석"):
                    korean_translations.append(line.split(": ", 1)[1])
            return english_conversations, korean_translations
        
        english_conversations, korean_translations = parse_conversation(answer)

        conversation = zip(english_conversations, korean_translations)

    return render_template("english.html", conversation=conversation)



if __name__ == '__main__':
    app.run(debug=True)