from datetime import datetime
from flask import Blueprint, render_template, request, url_for, flash
from werkzeug.utils import redirect
from .. import db
from lang.models import User, Conversation

from flask_login import current_user, login_required

from ..chat_model import ChatModel
from dotenv import load_dotenv
load_dotenv()

bp = Blueprint('lang', __name__, url_prefix='/lang')


@bp.route('/list/')
def _main():
    return render_template('langchain/lang.html')

@bp.route('/english/', methods=('GET','POST'))
def conversation():
    answer = None
    conversation = []
    past_conversations = []

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

        # 로그인한 상태라면 데이터베이스에 저장
        if current_user.is_authenticated:
            for eng,kor in conversation:
                new_conversation = Conversation(user_id=current_user.id, english=eng, korean=kor)
                db.session.add(new_conversation)
            try:
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                print("Error: ", e)
                flash("An error occurred while saving the conversation")
    if current_user.is_authenticated:
        past_conversations = Conversation.query.filter_by(user_id=current_user.id).all()

    return render_template('langchain/conversation.html', conversation=conversation, past_conversations=past_conversations)

@bp.route('/past/', methods=('GET','POST'))
def past_conv():
    return render_template('langchain/past_conv.html')