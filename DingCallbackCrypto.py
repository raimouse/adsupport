from Conf import *

class DingCallbackCrypto:
    def __init__(self,aes_key,app_key,aes_token):
        self.aes_key = aes_key
        self.app_key = app_key
        self.aes_token = aes_token

    #生成响应数据,默认为sucess
    def getEncryptedMap(self):
        encrypt = self.encrypt("success")
        timestamp = str(int(time.time()))
        nonce = self.generateRandomKey(16)
        sign = self.generateSignature(nonce, timestamp, self.aes_token,encrypt)
        return {'msg_signature':sign,'encrypt':encrypt,'timestamp':timestamp,'nonce':nonce}

    ##解密钉钉发送的数据
    def getDecryptMsg(self,msg_signature,timestamp,nonce,encrypt):
        #计算消息签名是否正确
        sign = self.generateSignature(nonce, timestamp, self.aes_token,encrypt)
        #print(sign, msg_signature)
        if msg_signature != sign:
            raise ValueError('signature check error')
        #首先对密文进行base64解码             
        content = base64.decodebytes(encrypt.encode('UTF-8'))  
        #初始向量为aes_key取前16位
        iv = self.aes_key[:16]
        #进行aes解密提取明文
        aesDecode = AES.new(self.aes_key, AES.MODE_CBC, iv)
        decodeRes = aesDecode.decrypt(content)
        padtext = decodeRes[-1]
        if padtext > 32:
            raise ValueError('Input is not padded or padding is corrupt')
        #去除填充字节
        decodeRes = decodeRes[:-padtext]
        #获取明文字符串长度
        length = struct.unpack('!i', decodeRes[16:20])[0]
        #校验尾部是否为对应的app_key
        if decodeRes[(20+length):].decode() != self.app_key:
            raise ValueError('corpId 校验错误')
        #提取明文消息体
        return decodeRes[20:(20+length)].decode()
    
    #加密明文
    def encrypt(self,encrypt):
        msg_len = self.getlength(encrypt)
        #拼接明文
        msg = ''.join([self.generateRandomKey(16) , msg_len.decode() , encrypt , self.app_key])
        #填充为16字节的倍数
        pad_msg = pad(msg.encode('utf-8'),AES.block_size)
        #初始向量iv为aes_key前16位
        iv = self.aes_key[:16]
        aesEncode = AES.new(self.aes_key, AES.MODE_CBC, iv)
        aesEncrypt = aesEncode.encrypt(pad_msg)
        #密文需要再进行一次base64加密
        return base64.encodebytes(aesEncrypt).decode('UTF-8')

    # 生成回调返回使用的签名值
    def generateSignature(self, nonce, timestamp, aes_token, encrypt):
        signList = ''.join(sorted([nonce, timestamp, aes_token, encrypt]))
        return hashlib.sha1(signList.encode()).hexdigest()

    #获取密文长度并转换为4字节编码
    def getlength(self, encrypt):
        length = len(encrypt)
        return struct.pack('>l', length)
    
    #生成加密所需要的随机字符串
    def generateRandomKey(self, size, chars=string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase + string.digits):
        return ''.join(choice(chars) for i in range(size))



#if __name__=='__main__':
#
#   dingCrypto = DingCallbackCrypto(aes_key,app_key,aes_token) 
#   msg = dingCrypto.getEncryptedMap()
#   print(msg)
  
