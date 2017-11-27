import pymysql.cursors


class DbMysql():
    def __init__(self, configs):
        self.configs = configs

    def start_con(self):
        self.con = pymysql.connect(**self.configs)

    def close(self):
        self.con.close()

    def save_one_data(self, tb_name, data,):
        '''
        将一条记录保存到数据库
        Args:
                                        tb_name: 表名字 str
                                        data:  记录 dict
        return:
                                        成功： dict 保存的记录
                                        失败： -1
        每条记录都以一个字典的形式传进来
        '''

        self.start_con()
        key_map = {}
        if len(data) == 0:
            return -1
        fields = ''
        values = ''
        datas = {}
        for k, v in data.items():
            # 防止SQL注入
            datas.update({k: pymysql.escape_string(v)})
        for d in datas:
            fields += "{},".format(str(d))
            values += "'{}',".format(str(data[d]))
        if len(fields) <= 0 or len(values) <= 0:
            return -1
            # 生产SQL语句
        # print(fields, values)
        sql = 'insert ignore into {}({}) values ({})'.format(
            tb_name, fields[:-1], values[:-1])
        try:
            with self.con.cursor() as cursor:
                cursor.execute(sql)
                self.con.commit()
        except Exception as e:
            print(e)
        self.close()

    def find_all(self, tb_name, limit_h=0, limit=-1):
        '''
        从数据库里查询所有记录
        Args:
                                        tb_name: 表名字 str
                                        limit: 限制数量
                                        当limit为-1的时候，从数据库取全部的数据
        return:
                                        成功: [dict]保存记录
                                        失败: -1
        '''

        try:
            self.start_con()
            with self.con.cursor() as cursor:
                if limit == -1 and limit_h == 0:
                    sql = "select * from {}".format(tb_name)
                else:
                    sql = "select * from {} limit {},{}".format(
                        tb_name, limit_h, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print("数据查询错误")
            return -1
        finally:
            self.close()

    def find_by_field(self, tb_name, field, field_value):
        '''
        从数据库里查询指定条件的记录
        Args:
                                        tb_name: 表名字 str
                                        field:   字段名
                                        field_value: 字段值
        return:
                                        成功: [dict] 保存的记录
                                        失败：-1
        '''

        try:
            self.start_con()
            with self.con.cursor() as cursor:
                sql = "select * from {} where {} = '{}'".format(
                    tb_name, field, field_value)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print("数据查询错误")
            return -1
        finally:
            self.close()

    def find_by_fields(self, tb_name, querset={}):
        '''
        从数据库里查询 符合多个条件的记录
        Args:
                                        tb_name 表名字 str
                                        queryset : key 字段 value 值 dict
        return:
                                        成功：[dict] 保存的记录
                                        失败：-1
        '''

        try:
            self.start_con()
            with self.con.cursor() as cursor:
                querrys = ""
                for k, v in querset.items():
                    querrys += "{} = '{}' and ".format(k, v)
                sql = "select * from {} where {} ".format(
                    tb_name, querrys[:-4])
                cursor.execute(sql)
                res = cursor.fetchall(sql)
                return res
        except:
            print('数据查询错误')
            return -1
        finally:
            self.con.close()

    def find_by_sort(self, table, field, limit=-1, order='DESC'):
        '''
        从数据库里查询排序过的数据
        Args:
                        table: 表名字 str
                        field: 字段名
                        limit: 限制数量
                        order: 降序DESC/升序ASC 默认为降序
        return:
                        成功： [dict] 保存的记录
                        失败： -1
        '''
        try:
            self.start_con()
            with self.con.cursor() as cursor:
                sql = "select * from {} order by {} {} limit 0,{}".format(
                    tb_name, field, order, limit)
                cursor.execute(sql)
                res = cursor.fetchall()
                return res
        except:
            print("数据查询错误")
            return -1
        finally:
            self.con.close()

    def find_count(self, table):
        try:
            self.start_con()
            with self.con.cursor() as cursor:
                sql = "select count(*) from {}".format(table)
                cursor.execute(sql)
                res = cursor.fetchone()
                return res
        except:
            print("数据查询错误")
        finally:
            self.con.close()
