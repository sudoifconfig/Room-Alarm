from dotenv import load_dotenv
import os

load_dotenv()


print("hello world")

password = os.getenv('TEST_PASSWORD')

print(password)

