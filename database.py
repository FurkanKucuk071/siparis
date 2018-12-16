import sqlite3

class DB(object):
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cur = self.conn.cursor()
        
        #Tablodaki kolon adları
        self.columns = ["Firma", "Sipariş No", "Sipariş Tarihi",  
                        "Sipariş Durumu", "Açıklama"] 
                        
        self.columns_lower = ', '.join([repr(col.lower()) for col in self.columns])
        
        self.create_table()

    def create_table(self):
        _string = 'CREATE TABLE IF NOT EXISTS siparisler ({})'
        sql = _string.format(self.columns_lower)
        self.cur.execute(sql)

    def insert_db(self, *args):
        _string = 'INSERT INTO siparisler VALUES (?, ?, ?, ?, ?)'
        sql = [_string, args[0]]
        self.cur.execute(*sql)
        self.conn.commit()
    
    def list_db(self, mode=0):
        '''
        mode=0: tüm siparişler
        mode=1: bekleyen siparişler
        mode=2: biten siparişler
        '''
        
        all_ord = 'SELECT * FROM siparisler'
        pending_ord = 'SELECT * FROM siparisler WHERE "sipariş durumu" = "Bekliyor"'
        completed_ord = 'SELECT * FROM siparisler WHERE "sipariş durumu" = "Bitti"'
        
        query_dict = {0: all_ord,
                      1: pending_ord,
                      2: completed_ord}
                      
        output = self.cur.execute(query_dict[mode])
        return output
        
    def update_db_item(self, sip_no, updated_record):
        #FIXME: Daha düzgün yazılacak...
        _string = '''update siparisler set 
                        "firma"= ?,
                        "sipariş no"= ?,
                        "sipariş tarihi"= ?, 
                        "sipariş durumu"= ?, 
                        "açıklama"= ?
                     where "sipariş no" = ?'''
        
        sql = [_string, [updated_record["firma"],
                         updated_record["sipariş no"],
                         updated_record["sipariş tarihi"],
                         updated_record["sipariş durumu"],
                         updated_record["açıklama"], str(sip_no)]]
        
        self.cur.execute(*sql)
        self.conn.commit()
        
    def delete_db_item(self, sip_no):
        _string = 'DELETE FROM siparisler WHERE "sipariş no" = ?'
        self.cur.execute(_string, (str(sip_no),))
        self.conn.commit()

    def close_db(self):
        self.conn.close()
        