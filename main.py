import libf
# curl http://localhost:11434/api/generate -d "{\"model\": \"qwen2.5:1.5b\", \"keep_alive\": 0}"

ollama_init = libf.ollama_lib()

while True:
    od = input("#指令: ")
    ollama_init.Order(od)