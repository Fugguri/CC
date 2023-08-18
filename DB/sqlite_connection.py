import sqlite3
from datetime import date


class Texts:
    def __init__(self, db_file) -> None:

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def set_new_text(self, text, comment_for_programmer=None, messanger_type=None):
        with self.connection:
            self.cursor.execute(
                f"INSERT OR IGNORE INTO texts ( text,comment_for_programmer,messanger_type) VALUES('{text}','{comment_for_programmer}','{messanger_type}')")
            self.connection.commit()

    def get_all_texts(self):
        with self.connection:
            self.cursor.execute("SELECT * FROM texts")
            rows = self.cursor.fetchall()
        return rows

    def get_text_by_id(self, text_id):
        with self.connection:
            c = self.cursor.execute(
                "SELECT text FROM texts WHERE id=?", (text_id,))
            rows = c.fetchone()[0]
        return rows

    def get_text_by_alias(self, text_id):
        with self.connection:
            c = self.cursor.execute(
                "SELECT * FROM texts WHERE id=?", (text_id,))
            rows = c.fetchone()
        return rows

    def delete_current_text(self, text_id):
        with self.connection:
            c = self.cursor.execute("DELETE FROM texts WHERE id=?", (text_id,))
            self.connection.commit()

    def delete_table(self):
        with self.connection:
            c = self.cursor.execute("DROP TABLE texts")
            self.connection.commit()

    def update_table(self):
        with self.connection:
            c = self.cursor.execute(
                "ALTER TABLE meetings ADD COLUMN status TEXT")
            self.connection.commit()

    def update_col_data(self, col_name: str, text: str, text_id: int | str):
        """_summary_

        Args:
            col_name (str): Название столбца
            text (str): Новый текст 
            text_id (int | str): id сообщения
        """
        with self.connection:
            data = (text, text_id)
            c = self.cursor.execute(
                f"UPDATE texts SET ({col_name}) = (?) WHERE id=?", data)
            self.connection.commit()


class Database(Texts):
    def __init__(self, db_file) -> None:

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def cbdt(self):
        with self.connection:
            create = """ CREATE TABLE IF NOT EXISTS houses
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                    cad_num TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                    house TEXT,
                    tenants TEXT,
                    owners TEXT,
                    meeting TEXT,
                    has_registry BOOLEAN DEFAULT false
                    );
                        CREATE TABLE IF NOT EXISTS meetings
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE ON CONFLICT IGNORE,
                    date_of_start TEXT,
                    date_of_end TEXT, 
                    secretary_full_name TEXT,
                    secretary_phone TEXT,
                    secretary_email TEXT,
                    bullyeten TEXT,
                    notification TEXT,
                    cad_num TEXT,
                    tenants TEXT,
                    owners TEXT,
                    status TEXT
                    );
                    CREATE TABLE IF NOT EXISTS texts
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT UNIQUE,
                    comment_for_programmer TEXT,
                    messanger_type TEXT
                    );
                    """
            self.cursor.executescript(create)

    def add_house(self, name, cad_num, house, tenants, owners):
        with self.connection:
            self.cursor.execute(
                f"INSERT INTO houses( name, cad_num,house,tenants,owners )VALUES('{name}', '{cad_num}','{house}', '{tenants}', '{owners}')"
            )
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS 'tenants{cad_num}'(id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date_of_create TEXT,
                    flat_num TEXT,
                    flat_id TEXT,
                    flat_status TEXT,
                    name TEXT,
                    phone TEXT,
                    has_watsapp TEXT,
                    status TEXT,
                    owner_full_name TEXT,
                    owner_email TEXT,
                    last_email_date TEXT,
                    last_oss_number TEXT,
                    date_of_sopd TEXT,
                    passport TEXT,
                    mkd_id TEXT,
                    fraction_part TEXT,
                    address TEXT,
                    owner TEXT,
                    cad_num TEXT
                    );""")
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS 'house{cad_num}'(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    status TEXT,
                    address TEXT,
                    number TEXT,
                    area TEXT,
                    cad_num TEXT UNIQUE ON CONFLICT IGNORE,
                    type TEXT,
                    floor TEXT,
                    entrance TEXT,
                    special_marks TEXT
                    );""")
            self.cursor.execute(
                f"""CREATE TABLE IF NOT EXISTS 'owners{cad_num}'
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     status TEXT,
                     cad_num TEXT,
                     number TEXT,
                     area TEXT,
                     numrator_of_the_share TEXT,
                     denominator_of_the_share TEXT,
                     lastname_or_legal_entity TEXT,
                     name_or_inn TEXT,
                     minddlename_or_orgn TEXT,
                     type_of_owner TEXT ,
                     num_request_statement TEXT,
                     query_date TEXT,
                     type_of_right TEXT,
                     state_registration_number TEXT ,
                     registration_date TEXT,
                     representative TEXT,
                     num_of_votes TEXT,
                     share_of_voises TEXT,
                     date_of_voise TEXT,
                     phone_num_owner TEXT,
                     email_owner TEXT,
                     ZHNS TEXT,
                     date_of_membership TEXT,
                     date_of_release TEXT,
                     type_of_representative TEXT,
                     representative_phone TEXT,
                     representative_email TEXT,
                     passport_seria TEXT,
                     date_of_birth TEXT,
                     date_of_sopd TEXT,
                     date_of_termination TEXT,
                     postal_address TEXT
                    );""")

    def add_house_data(self, cad_number, status, address, number, area, cad_num, type, floor, entrance, special_marks):
        with self.connection:
            self.cursor.execute(

                f"""INSERT INTO 'house{cad_number}'( status,address,number,area,cad_num,type,floor,entrance,special_marks ) 
                VALUES('{status}','{address}','{number}','{area}','{cad_num}','{type}','{floor}','{entrance}','{special_marks}')"""
            )
            self.connection.commit()

    def add_owner(self, cad_number,
                  status,
                  cad_num,
                  number,
                  area,
                  numrator_of_the_share,
                  denominator_of_the_share,
                  lastname_or_legal_entity,
                  name_or_inn,
                  minddlename_or_orgn,
                  type_of_owner,
                  num_request_statement,
                  query_date,
                  type_of_right,
                  state_registration_number,
                  registration_date,
                  representative,
                  num_of_votes,
                  share_of_voises,
                  date_of_voise,
                  phone_num_owner,
                  email_owner,
                  ZHNS,
                  date_of_membership,
                  date_of_release,
                  type_of_representative,
                  representative_phone,
                  representative_email,
                  passport_seria,
                  date_of_birth,
                  date_of_sopd,
                  date_of_termination,
                  postal_address):
        with self.connection:
            self.cursor.execute(
                f"""INSERT INTO 'owners{cad_number}'
                    (status,
                     cad_num,
                     number,
                     area,
                     numrator_of_the_share,
                     denominator_of_the_share,
                     lastname_or_legal_entity,
                     name_or_inn,
                     minddlename_or_orgn,
                     type_of_owner ,
                     num_request_statement,
                     query_date,
                     type_of_right,
                     state_registration_number ,
                     registration_date,
                     representative,
                     num_of_votes,
                     share_of_voises,
                     date_of_voise,
                     phone_num_owner,
                     email_owner,
                     ZHNS,
                     date_of_membership,
                     date_of_release,
                     type_of_representative,
                     representative_phone,
                     representative_email,
                     passport_seria,
                     date_of_birth,
                     date_of_sopd,
                     date_of_termination,
                     postal_address ) VALUES(
                     '{status}',
                     '{cad_num}',
                     '{number}',
                     '{area}',
                     '{numrator_of_the_share}',
                     '{denominator_of_the_share}',
                     '{lastname_or_legal_entity}',
                     '{name_or_inn}',
                     '{minddlename_or_orgn}',
                     '{type_of_owner}' ,
                     '{num_request_statement}',
                     '{query_date}',
                     '{type_of_right}',
                     '{state_registration_number}' ,
                     '{registration_date}',
                     '{representative}',
                     '{num_of_votes}',
                     '{share_of_voises}',
                     '{date_of_voise}',
                     '{phone_num_owner}',
                     '{email_owner}',
                     '{ZHNS}',
                     '{date_of_membership}',
                     '{date_of_release}',
                     '{type_of_representative}',
                     '{representative_phone}',
                     '{representative_email}',
                     '{passport_seria}',
                     '{date_of_birth}',
                     '{date_of_sopd}',
                     '{date_of_termination}',
                     '{postal_address}')"""
            )

    def add_tenant(self, tenant):

        tenant["last_email_date"] = ""
        tenant["last_oss_number"] = ""
        tenant["date_of_sopd"] = ""
        tenant["passport"] = ""
        with self.connection:
            self.cursor.execute(f"""INSERT INTO 'tenants{tenant["cad_num"]}'
                                (
                                date_of_create,
                                flat_num,
                                flat_id,
                                flat_status,
                                name,
                                phone,
                                has_watsapp,
                                status,
                                owner_full_name,                           
                                owner_email,
                                last_email_date,
                                last_oss_number,
                                date_of_sopd,
                                passport,
                                mkd_id,
                                fraction_part,
                                address,
                                owner,
                                cad_num)
                                VALUES(
                                '{tenant["date_of_create"]}',
                                '{tenant["flat_num"]}',
                                '{tenant["flat_id"]}',
                                '{tenant["flat_status"]}',
                                '{tenant["name"]}',
                                '{tenant["phone"]}',
                                '{tenant["has_watsapp"]}',
                                '{tenant["status"]}',
                                '{tenant["owner_full_name"]}',
                                '{tenant["owner_email"]}',
                                '{tenant["last_email_date"]}',
                                '{tenant["last_oss_number"]}',
                                '{tenant["date_of_sopd"]}',
                                '{tenant["passport"]}',
                                '{tenant["mkd_id"]}',
                                '{tenant["fraction_part"]}',
                                '{tenant["address"]}',
                                '{tenant["owner"]}',
                                '{tenant["cad_num"]}')""")

    def update_owner_representative(self, cad_num, representative, owner_id):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'owners{cad_num}' SET representative='{representative}' WHERE id='{owner_id}'""")

            self.connection.commit()

    def add_meeting(self, name, date_of_start, date_of_end, secretary_full_name, secretary_phone, secretary_email, bullyeten, notification, cad_num, tenants, owners, status):
        with self.connection:
            self.cursor.execute(f"""INSERT INTO meetings(
                    name,
                    date_of_start,
                    date_of_end, 
                    secretary_full_name,
                    secretary_phone,
                    secretary_email,
                    bullyeten,
                    notification,
                    cad_num,
                    tenants,
                    owners,
                    status
                    ) 
                    VALUES(
                    '{name}',
                    '{date_of_start}',
                    '{date_of_end}', 
                    '{secretary_full_name}',
                    '{secretary_phone}',
                    '{secretary_email}',
                    '{bullyeten}',
                    '{notification}',
                    '{cad_num}',
                    '{tenants}',
                    '{owners}',
                    '{status}'
                    )""")

    def all_houses(self):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM houses")

        return self.cursor.fetchall()

    def get_current_house(self, cad_num):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'houses' WHERE cad_num='{cad_num}' ")
        return self.cursor.fetchone()

    def get_all_houses(self,):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'houses'")

        return self.cursor.fetchall()

    def get_all_owners(self, cad_num):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'owners{cad_num}'")
        return self.cursor.fetchall()

    def get_house_data(self, cad_num, flat_num):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'house{cad_num}' WHERE number LIKE '%{flat_num}%' ")

        return self.cursor.fetchone()


    def get_house_by_id(self, id):
        with self.connection:
            self.cursor.execute(f"SELECT * FROM 'houses' WHERE cad_num=? ",(id,))
        return self.cursor.fetchone()


    def get_owner_by_full_name(self, cad_num, first_name, middle_name, last_name):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'owners{cad_num}' WHERE  'owners{cad_num}'.lastname_or_legal_entity=? AND 'owners{cad_num}'.name_or_inn=? AND 'owners{cad_num}'.minddlename_or_orgn=?   ", (first_name, middle_name, last_name))

        return self.cursor.fetchone()

    def get_house_by_can_num(self, cad_num):
        with self.connection:
            self.cursor.execute(
                f"SELECT count(`house{cad_num}`.name) FROM `house{cad_num}` LEFT JOIN houses on houses.cad_num=`{cad_num}` ")
            rows = self.cursor.fetchone()
            for row in rows:
                print(row)
            return rows

    def get_owners(self, cad_num, cur_flat_num):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'owners{cad_num}' WHERE number LIKE '%{cur_flat_num}%' ")
        return self.cursor.fetchall()

    def get_owner(self, cad_num, id):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM 'owners{cad_num}' WHERE id='{id}' ")
        return self.cursor.fetchone()

    def get_meeting_id(self, name):
        with self.connection:
            self.cursor.execute(
                f"SELECT id FROM meetings where name ={name}")
        return self.cursor.fetchone()

    def get_all_meetings(self):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM meetings")
        return self.cursor.fetchall()

    def get_meeting(self, name):
        with self.connection:
            self.cursor.execute(
                f"SELECT * FROM meetings WHERE name='{name}'")
        return self.cursor.fetchone()

    def get_meeting_by_name(self, name):
        with self.connection:
            self.cursor.execute(
                f"""SELECT *, houses.name FROM meetings 
                RIGHT JOIN houses USING(tenants)
                WHERE meetings.name=?
                """, (name,))
        return self.cursor.fetchone()

    def get_meeting_by_id(self, meeting_id):
        with self.connection:
            self.cursor.execute(
                f"""SELECT * ,houses.name FROM meetings 
                RIGHT JOIN houses USING(tenants)
                WHERE meetings.id={meeting_id} """)
        return self.cursor.fetchone()

    def get_houses_list(self):
        with self.connection:
            self.cursor.execute(
                """ SELECT * FROM houses """)

        return self.cursor.fetchall()

    def get_flat_with_letters(self, cad_num):
        with self.connection:
            self.cursor.execute(
                f""" SELECT number FROM 'house{cad_num}' 
                     WHERE number LIKE '%Y%' or number LIKE '%h%' or number LIKE '%y%' or number LIKE '%н%' or number LIKE '%Н%'
                """)

        return self.cursor.fetchall()

    def update_tenant_mailing_data(self, cad_num, date, name_of_oss, tenant_id):
        with self.connection:
            self.cursor.execute(
                f""" UPDATE `tenants{cad_num}` set (last_email_date,last_oss_number ) =(?,?) WHERE id=? ; """, (date, name_of_oss, tenant_id))
            self.connection.commit()

    def update_name(self):
        with self.connection:
            self.cursor.execute(
                """ UPDATE meetings
SET  (bullyeten,notification)
   = ('#_1-2023-Лит51_г.Санкт-Петербург, Литейный проспект, дом 51, литера А_бюллетень.docx','#_1-2023-Лит51_г.Санкт-Петербург, Литейный проспект, дом 51, литера А_сообщение.pdf')
WHERE id=4 ; """)
            self.connection.commit()
        return self.cursor.fetchall()

    def get_house_filling(self, house, tenants, owner):
        with self.connection:
            self.cursor.execute(
                f"""SELECT Count(*) FROM `{house}`""")
            house_ = self.cursor.fetchone()[0]
            self.cursor.execute(
                f"""SELECT Count(*) FROM `{owner}`""")
            owners = self.cursor.fetchone()[0]
            self.cursor.execute(
                f"""SELECT Count(*) FROM `{tenants}`""")
            tenants = self.cursor.fetchone()[0]
            self.cursor.execute(
                f"""
                SELECT meetings.name,  meetings.date_of_start, meetings.date_of_end, meetings.status
                FROM `{house}` 
                LEFT JOIN meetings ON meetings.cad_num=`{house}`.cad_num
                """)
        meeting = self.cursor.fetchone()
        if meeting:
            res = (house_, owners, tenants,
                   meeting[0], meeting[1], meeting[2], meeting[3])
            return res

    def get_house_by_cad_num(self, cad_num):
        try:
            with self.connection:
                self.cursor.execute(
                    """ SELECT name FROM houses WHERE cad_num like ?""", (cad_num,))

                house = self.cursor.fetchone()
                self.cursor.execute(
                    f""" SELECT count(*) FROM `house{cad_num}` """)
                count = self.cursor.fetchone()
                return (house[0], count[0],)
        except:
            return False

    def get_tenants_for_exel(self, cad_num):
        with self.connection:
            self.cursor.execute(f""" SELECT 
                                date_of_create,
                                flat_num,
                                flat_id,
                                flat_status,
                                name,
                                phone,
                                has_watsapp,
                                status,
                                owner_full_name,
                                fraction_part,                           
                                owner_email,
                                last_email_date,
                                last_oss_number,
                                date_of_sopd,
                                passport,
                                mkd_id
                                FROM 'tenants{cad_num}' """)
            tenants = self.cursor.fetchall()
            result = []
            for _ in tenants:
                part1 = _[:8]
                part2 = (_[8]+" "+_[9][:5]+"%",)
                part3 = _[10:]
                result.append(part1+part2+part3)
        return result

    def get_flats_for_exel(self, cad_num):
        with self.connection:
            self.cursor.execute(f""" SELECT 
                                h.entrance, h.floor, h.status, h.number, 
                                o.share_of_voises, 
                                t.name,t.status, t.phone, 
                                o.lastname_or_legal_entity, o.name_or_inn, o.minddlename_or_orgn,h.area,h.cad_num,t.has_watsapp,
                                o.num_of_votes, h.special_marks, o.representative
                                FROM 'house{cad_num}' as h 
                                FULL OUTER JOIN 'owners{cad_num}' as o USING (cad_num)
                                FULL OUTER JOIN 'tenants{cad_num}' as t ON t.owner= o.id
                                WHERE h.status NOT IN ('МКД', 'ЗУ', 'ОИ', 'ЛК')
                                """)

            flats = self.cursor.fetchall()
            result = []
            for flat in flats:
                print(flat)
                if flat[7] != None and flat[13] != None:
                    phone = flat[7]+f" ({flat[13]})"
                else:
                    phone = ""
                if flat[8] != None and flat[9] != None and flat[10] != None and flat[4] != None:
                    owner = str(flat[8] + " "+flat[9]+" " +
                                flat[10]+", " + flat[4])
                else:
                    owner = None
                if flat[11] != None:
                    square = flat[11].replace(".", ",")
                else:
                    square = None
                if flat[14] != None:
                    votes = flat[14].replace(".", ",")
                else:
                    votes = None

                if flat[6] != None:
                    status = flat[6]
                else:
                    status = None
                if flat[16] != "nan":
                    if status == None:
                        status = "Представитель"
                    status = f"{flat[16]} ({status})"
                else:
                    status = None
                data = (flat[0],
                        flat[1],
                        flat[2],
                        flat[3],
                        flat[4],
                        flat[5],
                        status,
                        phone,
                        owner,
                        flat[15],
                        square,
                        votes,
                        flat[12],
                        cad_num
                        )
                result.append(data)
        return result

    def get_receivers(self, meeting_id):
        with self.connection:
            self.cursor.execute(f""" SELECT tenants, owners 
                                FROM meetings 
                                WHERE id=?
                                """, (meeting_id,))
            tenants, owners = self.cursor.fetchone()
            self.cursor.execute(f""" SELECT t.owner_email, t.phone ,
                                o.cad_num, t.flat_num, o.lastname_or_legal_entity, o.name_or_inn , o.minddlename_or_orgn,
                                o.num_request_statement,o.query_date,o.state_registration_number,o.registration_date,
                                m.name, m.secretary_full_name,m.secretary_email, m.bullyeten, m.notification, houses.name,
                                o.number, o.area, t.name, o.representative
                                FROM 
                                '{tenants}' as t LEFT JOIN '{owners}' as o ON t.owner=o.id 
                                LEFT JOIN meetings as m ON m.cad_num=t.cad_num
                                LEFT JOIN houses USING (cad_num) 
                                WHERE m.id=? and (t.status='Собственник' or t.status='Представитель' ) 
                                """, (meeting_id,))
            result = self.cursor.fetchall()
        return result

    def delete_meeting(self, meeting_id):
        self.cursor.execute(f""" DELETE FROM meetings WHERE id={meeting_id}""")

    def delete_tenant(self, cad_num, tenant_id,):
        self.cursor.execute(
            f""" DELETE FROM 'tenants{cad_num}' WHERE id={tenant_id}""")
        self.connection.commit()

    def get_tenant_by_phone(self, cad_num, phone):
        with self.connection:
            self.cursor.execute(
                f""" select * FROM 'tenants{cad_num}' WHERE phone=?""", (phone,))
            return self.cursor.fetchone()

    def get_tenant_by_phone_in_all_house(self, cad_num, phone):
        with self.connection:
            self.cursor.execute(
                f"""SELECT tenants FROM 'houses'""")
            tenants_tables = self.cursor.fetchall()
            result = []
            for table in tenants_tables:
                query = f"SELECT * from `{table[0]}` WHERE phone={phone} "
                self.cursor.execute(query)
                res = self.cursor.fetchall()
                for i in res:
                    result.append(i)
        return result

    def get_meeting_and_tenant_for_notification_by_cad_num(self, cad_num, name, flat_num, phone, owner_fullname):
        with self.connection:
            self.cursor.execute(
                f""" select * FROM 'meetings' 
                LEFT JOIN `tenants{cad_num}` on `tenants{cad_num}`.name=? AND `tenants{cad_num}`.flat_num=? AND `tenants{cad_num}`.phone=? AND `tenants{cad_num}`.owner_full_name=?
                WHERE meetings.cad_num=? 
                """, (name, flat_num, phone, owner_fullname, cad_num))
            return self.cursor.fetchall()

    def get_receiver(self, cad_num, name, emailphone):
        with self.connection:
            self.cursor.execute(
                f""" select * FROM 'meetings' WHERE cad_num=?""", (cad_num,))
            return self.cursor.fetchone()

    def delete_house(self, house_id):
        self.cursor.execute(f""" SELECT tenants, owners,house,cad_num FROM houses WHERE id = {house_id}
                                """)
        tenants, owners, house, cad_num = self.cursor.fetchone()
        self.cursor.execute(
            f""" DELETE FROM meetings WHERE cad_num='{cad_num}'""")
        self.cursor.execute(
            f""" DELETE FROM houses WHERE id={house_id}""")
        self.cursor.execute(f""" DROP TABLE '{tenants}'""")
        self.cursor.execute(f""" DROP TABLE '{owners}'""")
        self.cursor.execute(f""" DROP TABLE '{house}'""")
        self.connection.commit()

    def is_phone_exist(self, phone):
        with self.connection:
            self.cursor.execute(
                f"""SELECT tenants FROM 'houses'""")
            tenants_tables = self.cursor.fetchall()
            try:
                query = ""
                query += f"SELECT * from `{tenants_tables[0][0]}` "
                for i in range(len(tenants_tables)):
                    if 0 < i:
                        query += f"\nleft join `{tenants_tables[i][0]}`"
                        query += f"USING (phone) "
                query += f"WHERE phone={phone} "

                self.cursor.execute(query)
            except:
                pass
        return self.cursor.fetchall()

    def check_email(self, cad_num, email):
        with self.connection:
            self.cursor.execute(f"""
                SELECT * FROM 'tenants{cad_num}' 
                WHERE owner_email='{email}' """)
        return self.cursor.fetchall()

    def update_email(self, phone=None, email=None):
        with self.connection:
            self.cursor.execute(
                f"""SELECT tenants FROM 'houses'""")
            tenants_tables = self.cursor.fetchall()
        for table in tenants_tables:
            with self.connection:
                self.cursor.execute(
                    f"UPDATE `{table[0]}` SET owner_email=? WHERE phone=?", (email, phone))
                self.connection.commit()

    def get_tenant_by_phone_for_email(self, phone=None, email=None):
        with self.connection:
            self.cursor.execute(
                f"""SELECT tenants FROM 'houses'""")
            tenants_tables = self.cursor.fetchall()
        result = []
        for table in tenants_tables:
            with self.connection:
                self.cursor.execute(
                    f"""SELECT * FROM meetings 
                    LEFT JOIN `{table[0]}` on meetings.cad_num=`{table[0]}`.cad_num
                    WHERE `{table[0]}`.phone=?""", (phone,))
                res = self.cursor.fetchall()
                for _ in res:
                    result.append(_)
        return result

    def get_tenant_by_flat(self, cad_num, flat_num):
        with self.connection:
            self.cursor.execute(f"""
                SELECT id, name,phone,status FROM 'tenants{cad_num}'WHERE flat_num=? """, (flat_num,))
        return self.cursor.fetchall()

    def get_tenant_by_id(self, cad_num, id):
        with self.connection:
            self.cursor.execute(f"""
                SELECT id, name,phone, owner_email, owner_full_name, address,flat_num,status,has_watsapp
                FROM 'tenants{cad_num}'WHERE id=? """, (id,))
        return self.cursor.fetchone()

    def update_tenant_owner(self, cad_num, tenant_id, owner_id, full_name):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'tenants{cad_num}' SET owner=?, owner_full_name=? WHERE id=?""", (owner_id, full_name, tenant_id))
            self.connection.commit()

    def update_tenant_status(self, cad_num, tenant_id, status):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'tenants{cad_num}' SET status=? WHERE id=?""", (status, tenant_id))
            self.connection.commit()

    def update_tenant_name(self, cad_num, tenant_id, status):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'tenants{cad_num}' SET name=? WHERE id=?""", (status, tenant_id))
            self.connection.commit()

    def update_tenant_phone(self, cad_num, tenant_id, phone, has_watsapp):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'tenants{cad_num}' SET phone=?, has_watsapp=? WHERE id=?""", (phone, has_watsapp, tenant_id))
            self.connection.commit()

    def update_tenant_email(self, cad_num, tenant_id, email):
        with self.connection:
            self.cursor.execute(
                f"""UPDATE 'tenants{cad_num}' SET owner_email=? WHERE id=?""", (email, tenant_id))
            self.connection.commit()

    def update_meeting_status(self, status, name=None, id=None):
        if name:
            with self.connection:
                self.cursor.execute(
                    """UPDATE meetings SET status=? WHERE name=?""", (status, name))
                self.connection.commit()
        if id:
            with self.connection:
                self.cursor.execute(
                    """UPDATE meetings SET status=? WHERE id=?""", (status, id))
                self.connection.commit()


if __name__ == "__main__":
    a = Database("CC.db")
    # a.update_table()
    # a.delete_house('14')
    # a.delete_house('3')
    # a.delete_house('43')
    # a.delete_house('56')
    a.delete_house('65')
    # a.delete_house('53')

    # a.delete_tenant("78:31:0001283:3019", "4")
