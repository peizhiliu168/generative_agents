"""
Author: Peizhi Liu (peizhiliu2023@u.northwestern.edu)

File: local_model.py
Description: Wrapper functions for local LLM APIs.
"""
import requests
import time

from utils import *

def LocalLLM_request(prompt, parameter):
    try:
        req = requests.post(local_model_host + "/api/generate", 
                            timeout=999, 
                            json={
                                "model":local_model_name,
                                "prompt":prompt,
                                "stream":parameter["stream"],
                                "eval_count":parameter["max_tokens"],
                                "options": {
                                    "temperature":parameter["temperature"],
                                    "top_p":parameter["top_p"],
                                    "frequency_penalty":parameter["frequency_penalty"],
                                    "presence_penalty":parameter["presence_penalty"],
                                    "stop":parameter["stop"]
                                }
                            })
        
        if req.status_code != 200:
            raise Exception("LLM Completion excpetion")
        
        resp = req.json()
        text = resp['response']
        return text
        
    except:
        print ("TOKEN LIMIT EXCEEDED")
        return "TOKEN LIMIT EXCEEDED"

def ChatLocalLLM_request(prompt):
    try:
        req = requests.post(local_model_host + "/api/chat",
                                timeout=999,
                                json={
                                    "model":local_model_name,
                                    "messages":[
                                        {
                                            "role":"user",
                                            "content":prompt
                                        }
                                    ],
                                    "stream":False})
        
        if req.status_code != 200:
            raise Exception("LLM Chat excpetion")

        resp = req.json()
        text = resp['message']['content']
        return text

    except:
        print ("Chat LLM ERROR")
        return "Chat LLM ERROR"

def temp_sleep(seconds=0.1):
  time.sleep(seconds)

def ChatLocalLLM_single_request(prompt): 
    req = requests.post(local_model_host + "/api/chat",
                        timeout=999,
                        json={
                            "model":local_model_name,
                            "messages":[
                                {
                                    "role":"user",
                                    "content":prompt
                                }
                            ],
                            "stream":False})
        
    if req.status_code != 200:
        raise Exception("LLM Chat excpetion")

    resp = req.json()
    text = resp['message']['content']
    return text

def get_LocalLLM_embedding(text):
    req = requests.post(local_model_host + "/api/embeddings",
                        timeout=999,
                        json={
                            "model":local_model_name,
                            "prompt":text
                            })
        
    if req.status_code != 200:
        raise Exception("LLM Embedding excpetion")

    resp = req.json()
    embedding = resp['embedding']
    return embedding


if __name__ == '__main__':
    gpt_param = {"engine": "text-davinci-003", "max_tokens": 500, 
                "temperature": 1, "top_p": 1, "stream": False,
                "frequency_penalty": 0, "presence_penalty": 0, "stop": None}
    get_LocalLLM_embedding("hello")