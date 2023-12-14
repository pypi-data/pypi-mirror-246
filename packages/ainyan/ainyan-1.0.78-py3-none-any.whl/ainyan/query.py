import argparse
import configparser
from flask import Flask, json, request
import json

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline


def post_query(model, tokenizer, config, prompt_mode, web_mode):
    config_queries = config["queries"]
    string_list_str = config_queries.get('texts')
    string_list = string_list_str.split(', ')
    # https://huggingface.co/docs/transformers/main_classes/text_generation#transformers.GenerationConfig
    temperature = config_queries.getfloat("temperature", fallback=1.0)
    repetition_penalty = config_queries.getfloat("repetition_penalty", fallback=1.0)
    top_k = config_queries.getint("top_k", fallback=50)
    max_length = config_queries.getint("max_length", fallback=50)

    prompt = pipeline(task="text-generation",
                      model=model,
                      tokenizer=tokenizer,
                      temperature=temperature,
                      repetition_penalty=repetition_penalty,
                      top_k=top_k,
                      max_length=max_length)

    if web_mode is not None and web_mode == True:
        api = Flask(__name__)

        @api.route('/prompt', methods=['GET'])
        def query():
            query = request.args.get('query')
            return prompt(query)[0]['generated_text']

        api.run()

    if prompt_mode is not None:
        input_ = input("> ")
        while input_ != "q":
            if len(input_) < 3:
                print("Input too short")
            else:
                prompt_and_print(prompt, input_, False)
            input_ = input("> ")
    else:
        for query in string_list:
            prompt_and_print(prompt, query, True)


def prompt_and_print(prompt, query, echo):
    if echo is True:
        print("----\n" + query + "\n----\n")
    print(prompt(query)[0]['generated_text'] + "\n")
    if echo is True:
        print("\n----\n")
    else:
        print("\n")



def main():
    parser = argparse.ArgumentParser(description='Training facilitator')
    parser.add_argument('--config', metavar='config', required=True,
                        help='the path to the ini file used for queries')
    parser.add_argument('--model', metavar='model', required=True,
                        help='override the name defined in the ini file')
    parser.add_argument('--prompt', required=False,
                        help='run in prompt mode', action='store_true')
    parser.add_argument('--web', required=False,
                        help='run in web mode', action='store_true')
    args = parser.parse_args()

    config_file = args.config
    model = args.model + ""

    config = configparser.ConfigParser()
    config.read(config_file)

    print("Using training file:" + config_file + " ; loading model:" + model + "\n")

    tokenizer = AutoTokenizer.from_pretrained(model, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(model, trust_remote_code=True)

    post_query(model, tokenizer, config, args.prompt, args.web)


if __name__ == '__main__':
    main()
