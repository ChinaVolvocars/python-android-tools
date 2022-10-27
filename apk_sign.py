'''
apksigner sign                 //执行签名操作
--ks 你的jks路径               //jks签名证书路径
--ks-key-alias 你的alias          //生成jks时指定的alias
--ks-pass pass:你的密码           //KeyStore密码
--key-pass pass:你的密码          //签署者的密码，即生成jks时指定alias对应的密码
--out output.apk               //输出路径
input.apk                   //需要签名的APK
'''

'''
apksigner verify -v --print-certs xxx.apk
参数:
 -v, --verbose 显示详情(显示是否使用V1和V2签名)
--print-certs 显示签名证书信息
 
例如:
apksigner verify -v xxx.apk
 
Verifies
Verified using v1 scheme (JAR signing): true
Verified using v2 scheme (APK Signature Scheme v2): true
Number of signers: 1
'''

import shutil
import os

"""
1.安装Python3.10，配置环境变量。
2.配置apksinger的环境变量。
3.把xxx.jks、xxx.apk（支持多个）放入和apk_sign.py同目录下。
4.双击apk_sign.py，出现命令行窗体，等待。
5.按任意键结束。
6.查看output目录下已签好的apk文件。
"""
# jks签名证书（放在当前目录中）
jksFile = 'iscan.jks'
# KeyStore密码
storePassword = '123456'
# 生成jks时指定的alias
keyAlias = 'keyali'
# 签署者的密码，即生成jks时指定alias对应的密码
keyPassword = '123456'

# 获取当前目录中所有的apk源包
src_apks = []


# python3 : os.listdir()即可，这里使用兼容Python2的os.listdir('.')
def apk_sign():
    for file in os.listdir('.'):
        if os.path.isfile(file):
            extension = os.path.splitext(file)[1][1:]
            if extension in 'apk':
                src_apks.append(file)
    for src_apk in src_apks:
        # file name (with extension)
        src_apk_file_name = os.path.basename(src_apk)
        # 分割文件名与后缀
        temp_list = os.path.splitext(src_apk_file_name)
        # name without extension
        src_apk_name = temp_list[0]
        # 后缀名，包含.   例如: ".apk "
        src_apk_extension = temp_list[1]
        # 创建生成目录
        output_dir = 'output/'
        # 目录不存在则创建
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)
        # 目标文件路径
        target_apk = output_dir + src_apk_name + src_apk_extension
        # 签名后的文件路径
        signer_apk = output_dir + src_apk_name + '_signer' + src_apk_extension
        # 拼装签名命令
        signer_str = 'apksigner sign --ks ' + jksFile + ' --ks-pass pass:' + storePassword + ' --ks-key-alias ' + keyAlias + ' --key-pass pass:' + keyPassword + ' --out ' + signer_apk + ' ' + src_apk
        # 执行签名命令
        with os.popen(signer_str, "r") as p:
            r = p.read()
            print('### signer success ###: %s' % r)
        # 输出签名命令执行结果
        # 拼装验证签名命令
        verify_str = 'apksigner verify -v --print-certs ' + signer_apk
        # 执行对签过的apk进行签名验证
        with os.popen(verify_str, "r") as p:
            r = p.read()
            print('verify_result:\t', r)
        # 输出验证签名命令执行结果
        # os.remove(target_apk)


if __name__ == '__main__':
    apk_sign()
