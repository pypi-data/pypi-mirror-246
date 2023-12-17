from colorama import init #only this one is needed from the original colorama
init()
from ansi_ex_fore import Fore_EX
from ansi_ex_back import Back_EX

for i in Fore_EX.__dict__.values():
    print(i + "Hello, Colorama_EX!")

for j in Back_EX.__dict__.values():
    print(j + "Hello again, Colorama_EX!")