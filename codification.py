from os import getcwd

class Codification:
    def transform_str_ascii(self,message,key):
        ascii_message = []
        ascii_key = []
        for letter in message:
            ascii_message.append(ord(letter))

        for letter in key:
            ascii_key.append(ord(letter))
            
        return ascii_message, ascii_key
    
    def transform_decimal_binary(self,num: int):
        binary_number = ''
        while num != 0:
            binary_number = str(num % 2) + binary_number
            num = num // 2
        return binary_number

    def transform_strBin_arrayBin(self,num: str):
        array_number = list(map(lambda el: int(el), num))
        return array_number[::-1]

    def transform_binary_decimal(self,num: str):
        binNumber = self.transform_strBin_arrayBin(num)
        #print(binNumber)
        decimal_number = 0
        for pos,value in enumerate(binNumber):
            decimal_number += value*(pow(2,pos))
        return decimal_number

    def xor_operation(self,num1,num2):
        if num1 == num2:
            return 0
        else:
            return 1
        
    def codec_word(self,message_letter,key_letter):
        message_output = ''
        if len(message_letter) > len(key_letter):
            key_letter = '0'*(len(message_letter)-len(key_letter)) + key_letter
        elif len(message_letter) < len(key_letter):
            message_letter = '0'*(len(key_letter)-len(message_letter)) + message_letter

        for pos,value in enumerate(message_letter):
            message_output += str(self.xor_operation(value,key_letter[pos]))
        return message_output

    def encript_message(self,message,key):
        try:
            with open(getcwd() + "/key.des", "w") as keyfile:
                keyfile.write(key)
                keyfile.close()
    
            ascii_message, ascii_key = self.transform_str_ascii(message,key)
            transformed_input = list(map(lambda code: self.transform_decimal_binary(code), ascii_message))
            transformed_key = list(map(lambda code: self.transform_decimal_binary(code), ascii_key))

            encripted_message = []
            key_pos = 0
            for letter in transformed_input:
                encripted_message.append(self.codec_word(letter, transformed_key[key_pos]))
                key_pos += 1
                if key_pos == len(transformed_key):
                    key_pos = 0

            message_output = ""
            for bin_number in encripted_message:
                character_ascii_code = self.transform_binary_decimal(bin_number)
                message_output += chr(character_ascii_code)
            
            bytes_message = bytes(message_output, 'utf-8')
            with open(getcwd()+"/encripted.des", 'wb') as archivo:
                archivo. write(bytes_message)
                archivo.close()
            return True
        except Exception as e:
            return False
    
    def desencript_message(self,encripted_message):
        try:
            with open(getcwd()+"/key.des", 'rb') as archivo:
                lineas_archivo = archivo.readlines()
                key =''.join(list(map(lambda le : str(le, 'utf-8'),lineas_archivo)))
                archivo.close()

            ascii_message, ascii_key = self.transform_str_ascii(encripted_message,key)
            transformed_message_encripted = list(map(lambda code: self.transform_decimal_binary(code), ascii_message))
            transformed_key = list(map(lambda code: self.transform_decimal_binary(code), ascii_key))
            
            desencripted_message = []
            key_pos = 0
            for letter in transformed_message_encripted:
                desencripted_message.append(self.codec_word(letter, transformed_key[key_pos]))
                key_pos += 1
                if key_pos == len(transformed_key):
                    key_pos = 0
            
            message_output = ""
            for bin_number in desencripted_message:
                character_ascii_code = self.transform_binary_decimal(bin_number)
                message_output += chr(character_ascii_code)
            
            with open(getcwd()+"/desencripted_message.txt", 'w') as archivo:
                archivo. write(message_output)
                archivo.close()
            return True
        except Exception as e:
            return False

    