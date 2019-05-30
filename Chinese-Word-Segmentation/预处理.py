#!/usr/bin/env python  
#-*-coding:utf-8-*-     
#4-tags for character tagging: B(Begin),E(End),M(Middle),S(Single)
#解决中括号大词组分词问题
#解决换行引起的分离问题
#区分标点符号和数字，标点符号按ｓ标注，数字不标注
#解决无汉字的标注问题
#解决姓名拼接问题
import codecs  
import sys        
def character_tagging(input_file, output_file):  
    input_data = codecs.open(input_file, 'r', 'utf-8')  
    output_data = codecs.open(output_file, 'w', 'utf-8')
    tail=""
    #定义汉字判别函数
    def is_chinese(char):
        if char >= '\u4e00' and char <= '\u9fa5':
            return True
        else:
            return False 
    #读取数据      
    for line in input_data.readlines():  
        line = line.strip('\r\n\t')
        if line=="":
            continue
        word_list = line.strip().split()
        #处理换行导致分离问题
        word_list[0]=word_list[0]+tail
        if word_list[-1][-1].isalpha:
            tail=""
        else:
            tail=word_list[-1]
        
        for i in range(len(word_list)):
            #处理中括号带来的大词组问题
            if word_list[i].find('[')>=0:
                word_list[i]=word_list[i][1:]
            if word_list[i].find(']')>=0:
                word_list[i]=word_list[i][:word_list[i].find(']')]
            #处理不含汉字问题，先定向'/'
            index=word_list[i].find('/')
            #标点符号以ｓ直接输出
            if index<=1 and is_chinese(word_list[i][0])==False:
                output_data.write(word_list[i][0] + "\tS\n")
                continue
            #寻找最近的汉字
            for j in range(index+2):          
                if is_chinese(word_list[i][j])==True:
                    word_list[i]=word_list[i][j:]
                    break
            #重新定向'/'
            index=word_list[i].find('/')
            #无汉字的不处理
            if j>=index:
                continue
            #姓名拼接问题
            if word_list[i].endswith('nr') and i+1<=len(word_list)-1:
                word_list[i]=word_list[i][:index]+word_list[i+1]
                index=word_list[i].find('/')
            #普通情况正常处理
            if len(word_list[i][:index]) == 1:  
                output_data.write(word_list[i][0] + "\tS\n")  
            else:  
                output_data.write(word_list[i][0] + "\tB\n")  
                for j in range(1,index-1):
                    output_data.write(word_list[i][j] + "\tM\n")  
                output_data.write(word_list[i][index-1] + "\tE\n")
            if word_list[i].endswith('nr') and i+1<=len(word_list)-1:
                word_list[i+1]="##/pass"
            #每段落结束
        output_data.write("\n")  
    input_data.close()  
    output_data.close()  
      
if __name__ == '__main__':  
    if len(sys.argv) != 3:  
        print ("Usage: python " + sys.argv[0] + " input output")  
        sys.exit(-1)  
    input_file = sys.argv[1]  
    output_file = sys.argv[2]  
    character_tagging(input_file, output_file) 



