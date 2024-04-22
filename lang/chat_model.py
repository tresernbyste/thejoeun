from langchain_openai import ChatOpenAI
from langchain_openai import ChatOpenAI 
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

class ChatModel:
    def __init__(self, model_name="gpt-3.5-turbo", max_tokens=2048, temperature=0):
        self.model_name = model_name
        self.max_tokens = max_tokens
        self.temperature = temperature

    def generate_response(self):
        model = ChatOpenAI(
            model=self.model_name,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        template = """
        당신은 영어를 가르치는 10년차 영어 선생님입니다. 상황에 [FORMAT]에 영어 회화를 5가지 작성해 주세요. 

        상황:
        {question}

        FORMAT:
        각 대화 예제는 다음 형식에 맞춰 주세요:

        영어 회화 1: [여기에 영어 회화 내용]
        한글 해석 1: [여기에 한글 해석 내용]

        영어 회화 2: [여기에 영어 회화 내용]
        한글 해석 2: [여기에 한글 해석 내용]

        영어 회화 3: [여기에 영어 회화 내용]
        한글 해석 3: [여기에 한글 해석 내용]

        영어 회화 4: [여기에 영어 회화 내용]
        한글 해석 4: [여기에 한글 해석 내용]

        """
        prompt = PromptTemplate.from_template(template)

        output_parser = StrOutputParser()

        chain = prompt | model | output_parser
        return chain