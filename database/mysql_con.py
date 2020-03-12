import mysql.connector.pooling

class Mysql_Database(object):
    def __init__(self):
        self.config = {
            'host':'127.0.0.1',
            'port':'3304',
            'user':'root',
            'password':'123456',
            'database':'shuquge'
        }
        self.pool = mysql.connector.pooling.MySQLConnectionPool(
            **self.config,pool_size=20
        )
        self.con = self.pool.get_connection()

    def insert_data(self,**data):
        sql = 'insert ignore into jianjie (id,书名,作者,分类,状态,字数,更新时间,封面,简介)' \
              'values({id},"{书名}","{作者}","{分类}","{状态}",{字数},"{更新时间}","{封面}","{简介}");'.format_map(data)
        print(sql)
        self.con.start_transaction()
        cursor = self.con.cursor()
        cursor.execute(sql)
        self.con.commit()
        self.con.close()

if __name__=='__main__':
    data = {
        'id': 5806, '书名': '元尊', '作者': '天蚕土豆', '分类': '玄幻魔法', '状态': '连载中', '字数': 2025827,
        '更新时间': '2019-11-19 20:30:01','简介':'进击','封面':'进击'
        # 'id':6,'书名':'进击', '作者':'进击', '分类':'进击', '状态':'进击', '字数':2, '更新时间':2000, '封面':'封面','简介':'看看'
    }
    test = Mysql_Database()
    test.insert_data(**data)





