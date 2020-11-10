

def Num2String(integer):
    CharSet = "+-0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    #This is Xxencoding, it was chosen so that the string could be a file name
    string = ""
    while integer != 0:
        integer, CharCode = divmod(integer,64)
        string = CharSet[CharCode] + string
    return(string)




def String2Num(string):
    CharSet = {'+':0,'-':1,'0':2,'1':3,'2':4,'3':5,'4':6,'5':7,'6':8,'7':9,
               '8':10,'9':11,'A':12,'B':13,'C':14,'D':15,'E':16,'F':17,'G':18,'H':19,
               'I':20,'J':21,'K':22,'L':23,'M':24,'N':25,'O':26,'P':27,'Q':28,'R':29,
               'S':30,'T':31,'U':32,'V':33,'W':34,'X':35,'Y':36,'Z':37,'a':38,'b':39,
               'c':40,'d':41,'e':42,'f':43,'g':44,'h':45,'i':46,'j':47,'k':48,'l':49,
               'm':50,'n':51,'o':52,'p':53,'q':54,'r':55,'s':56,'t':57,'u':58,'v':59,
               'w':60,'x':61,'y':62,'z':63,}
    power = len(string) - 1
    integer = 0
    for character in string:
        CharCode = CharSet[character]
        CharCode = CharCode * (64 ** power)
        integer += CharCode
        power -= 1
    return(integer)

def GetKHash(PublicKeyID):
    with open("WiFall Key") as WiFallKey:
        WFK = WiFallKey.read() #Save the contents of the WiFall Key file to WFK
    with sqlite3.connect("data.db") as database:
        query = "SELECT salt FROM keys WHERE PublicKeyID = (?)"
        print(query)
        for row in database.execute(query,[PublicKeyID]):
            print(row)
            salt = row[0]    
    KHash = Hash(WFK,salt)
    return(KHash)




print(Num2String(1519242))
print(String2Num("3mu8"))