from http import HTTPStatus
import dashscope
import os


dashscope.api_key = "sk-edc4fb494e6446cf9bb77bb181e77b07"


def get_answer(prompt):

    print(f"AI问答: {prompt}")
    messages = [
        {'role': 'user',
         'content': f'{prompt}'}
    ]
    response = dashscope.Generation.call("qwen-max",
                                          messages=messages,
                                          result_format='message',
                                          stream=False,
                                          incremental_output=False
                                          )

    if response.status_code == HTTPStatus.OK:
        content = response.output.choices[0]['message']['content']
    else:
        content = "AI回答暂不可用"
        print(f'Request id: {response.request_id}, Status code: {response.status_code}, '
              f'error code: {response.code}, error message: {response.message}')
    print("AI回答:", content.encode('utf-8').decode('utf-8'))
    # 返回指定格式的结果
    return content


if __name__ == '__main__':
    prompt = ""
    result = get_answer(prompt)
    print("AI回答:", result)
