from jsslib import JSS

if __name__ == '__main__':

    jss = JSS(log_level=1)
    jss.CreateTable('../../release/lang/table/zi.json', '../../../data/jss/lang/json/zi', '../../../data/jss/lang/table/zi')
    
    jss.LoadTable('../../../data/jss/lang/table/zi')
    print(jss.RunSql("SELECT TOP 10 id, Zi FROM zi WHERE PinYin = 'ding1' and id > 2;"))
