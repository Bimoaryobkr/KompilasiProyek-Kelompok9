from distutils.log import error
import kelompok9

while True:
    text=input('Kelompok9 > ')
    result, error=kelompok9.Run(text)

    if error: print(error.as_string())
    else: print(result)