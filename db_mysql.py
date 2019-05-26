import MySQLdb

hostname = "localhost"
username = "root"
password = ""
db_name  = "drama_ojol"

# Open database connection
db = MySQLdb.connect(hostname,username,password,db_name)
db.set_character_set('utf8')

# prepare a cursor object using cursor() method
cursor = db.cursor()
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

def executeSql(sql):
    return cursor.execute(sql);

def fetch(type='all'):
    if type=='all':
        return cursor.fetchall();
    else:
        return cursor.fetchone();
def commit():
    db.commit();

def escapeString(string):
    return MySQLdb.escape_string(string);

def existSentimentalWord(word):
    sql = '''SELECT * 
                FROM memory_word
                WHERE word="%s" AND type is not NULL AND value is not NULL''' \
                % (word);
    cursor.execute(sql);
    return cursor.fetchone();

def existSentimentalWordMainObject(word):
    sql = '''SELECT * 
                FROM apps_memory_word
                WHERE word="%s" AND value is not NULL''' \
                % (word);
    cursor.execute(sql);
    return cursor.fetchone();

def existOtherKamus(word):
    sql = '''SELECT * 
                FROM tb_katadasar
                WHERE word="%s"''' \
                % (word);
    cursor.execute(sql);
    return cursor.fetchone();

def insertUnknownWord(word):
    if len(word) < 20:
        sql = '''SELECT * 
                    FROM unknown_word
                    WHERE word="%s"''' \
                    % (word);
        cursor.execute(sql);
        result = cursor.fetchone();
        if result == None:
            sql = '''INSERT INTO unknown_word(word)
                        VALUES ('%s')'''\
                        % (word);
            cursor.execute(sql);
            db.commit();
        else:
            new_frequent = result[4] + 1;
            sql = '''UPDATE unknown_word SET frequently=%d 
                        WHERE id=%d ''' % (new_frequent,result[0]);
            cursor.execute(sql);
            db.commit();

def existStoplist(word):
    sql = '''SELECT * 
                FROM memory_stopword
                WHERE word="%s"''' \
                % (word);
    cursor.execute(sql);
    return cursor.fetchone();

def getMemoryGroupWord():
    sql = '''SELECT word 
                FROM memory_word WHERE word LIKE "% %"''';
    cursor.execute(sql);
    result = cursor.fetchall();
    return result;

def getOtherMemoryGroupWord():
    sql = '''SELECT word 
                FROM apps_memory_word WHERE word LIKE "% %"''';
    cursor.execute(sql);
    result = cursor.fetchall();
    return result;