import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
import os


def create_user_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE users ("
               "userid INTEGER, "
               "username TEXT NOT NULL, "
               "role TEXT, "
               "passwordhash TEXT NOT NULL, "
               "PRIMARY KEY(userid) "
               "UNIQUE(username))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


def create_products_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE products ("
               "productid INTEGER, "
               "name TEXT NOT NULL, "
               "price INTEGER NOT NULL, "
               "imgpath TEXT,"
               "shortdesc TEXT,"
               "desc TEXT,"
               "PRIMARY KEY(productid))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


def insert_product(conn, name, price, imgpath, shortdesc, desc):
    """Add products."""
    cur = conn.cursor()
    try:
        sql = (
            "INSERT INTO products (name, price, imgpath, shortdesc, desc) VALUES (?,?,?,?,?)")
        cur.execute(sql, (name, price, imgpath, shortdesc, desc))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Product {} added with id {}.".format(name, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


def update_product(conn, name, price, imgpath, shortdesc, desc, productid):
    """Update product"""
    cur = conn.cursor()
    try:
        sql = ("UPDATE products SET "
               "name=?, price=?, imgpath=?, shortdesc=?,desc=? "
               "WHERE productid = ?")
        cur.execute(sql, (name, price, imgpath, shortdesc, desc, productid))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Updated product {}.".format(productid))
        return productid
    finally:
        cur.close()


def delete_product(conn, productid):
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM products "
               "WHERE productid = ?")
        cur.execute(sql, (productid,))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Removed product {}.".format(productid))
        return cur.rowcount
    finally:
        cur.close()


def get_products(conn):
    """Get products."""
    cur = conn.cursor()
    try:
        sql = ("SELECT * FROM products")
        cur.execute(sql)
        products = []
        for row in cur:
            (id, name, price, imgpath, shortdesc, desc) = row
            products.append({
                "id": id,
                "name": name,
                "price": price,
                "imgpath": imgpath,
                "shortdesc": shortdesc,
                "desc": desc
            })
        return products
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_product_by_id(conn, id):
    """Get product."""
    cur = conn.cursor()
    try:
        sql = ("SELECT * FROM products WHERE productid=?")
        cur.execute(sql, (id,))
        row = cur.fetchone()

        return {
            "id": row[0],
            "name": row[1],
            "price": row[2],
            "imgpath": row[3],
            "shortdesc": row[4],
            "desc": row[5]
        }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def add_user(conn, username, hash, role="normal user"):
    """Add user. Returns the new user id"""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO users (username,role , passwordhash) VALUES (?,?,?)")
        cur.execute(sql, (username, role, hash))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("User {} created with id {}.".format(username, cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()


def get_user_by_name(conn, username):
    """Get user details by name."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username, role FROM users WHERE username = ?")
        cur.execute(sql, (username,))
        for row in cur:
            (id, name, role) = row
            return {
                "username": name,
                "userid": id,
                "role": role
            }
        else:
            # user does not exist
            return {
                "username": username,
                "userid": None,
                "role": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_user_by_id(conn, userid):
    """Get user details by id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT userid, username, role FROM users WHERE userid = ?")
        cur.execute(sql, (userid,))
        for row in cur:
            (id, name, role) = row
            return {
                "username": name,
                "userid": id,
                "role": role
            }
        else:
            # user does not exist
            return {
                "username": None,
                "userid": None,
                "role": None
            }
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def get_hash_for_login(conn, username):
    """Get user details from id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT passwordhash FROM users WHERE username=?")
        cur.execute(sql, (username,))
        for row in cur:
            (passhash,) = row
            return passhash
        else:
            return None
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def create_cart_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE cart ("
               "userid INTEGER, "
               "productid INTEGER, "
               "quantity INTEGER, "
               "UNIQUE (userid,productid),"
               "FOREIGN KEY (productid) REFERENCES products (productid),"
               "FOREIGN KEY (userid) REFERENCES users(userid))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


def get_cart_by_id(conn, userid):
    """Get cart details by id."""
    cur = conn.cursor()
    try:
        sql = ("SELECT * FROM cart WHERE userid = ?"
              "ORDER BY rowid")
        cur.execute(sql, (userid,))
        cart = []
        for row in cur:
            (id, productid, quantity) = row
            cart.append({
                "userid": id,
                "quantity": quantity,
                "product": get_product_by_id(conn, productid)
            })
        return cart
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    finally:
        cur.close()


def insert_into_cart(conn, userid, productid, quantity):
    """Add to cart."""
    cur = conn.cursor()
    try:
        sql = ("INSERT OR REPLACE INTO cart (userid, productid, quantity) VALUES (?,?,?)")
        cur.execute(sql, (userid, productid, quantity))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("Product {} added to user {} cart.".format(productid, userid))
        return cur.lastrowid
    finally:
        cur.close()


def remove_from_cart(conn, userid, productid):
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM cart "
               "WHERE productid = ? AND userid = ?")
        cur.execute(sql, (productid, userid))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Removed {} item.".format(cur.rowcount))
        return cur.rowcount
    finally:
        cur.close()


def remove_all_from_cart(conn, userid):
    cur = conn.cursor()
    try:
        sql = ("DELETE FROM cart "
               "WHERE userid = ?")
        cur.execute(sql, (userid,))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return 0
    else:
        print("Removed item for user {}.".format(userid))
        return cur.rowcount
    finally:
        cur.close()


def create_orders_table(conn):
    """Create table."""
    cur = conn.cursor()
    try:
        sql = ("CREATE TABLE orders ("
               "firstname TEXT, "
               "lastname TEXT, "
               "email TEXT,"
               "street TEXT,"
               "city TEXT,"
               "postcode INTEGER,"
               "products TEXT NOT NULL,"
               "orderid INTEGER,"
               "PRIMARY KEY (orderid))")
        cur.execute(sql)
        conn.commit
    except sqlite3.Error as err:
        print("Error: {}".format(err))
    else:
        print("Table created.")
    finally:
        cur.close()


def insert_into_orders(conn, firstname, lastname, email, street, city, postcode, products):
    """Add to orders."""
    cur = conn.cursor()
    try:
        sql = ("INSERT INTO orders (firstName, lastName, email,street,city,postCode,products) VALUES (?,?,?,?,?,?,?)")
        cur.execute(sql, (firstname, lastname, email,
                    street, city, postcode, products))
        conn.commit()
    except sqlite3.Error as err:
        print("Error: {}".format(err))
        return -1
    else:
        print("added order {}.".format(cur.lastrowid))
        return cur.lastrowid
    finally:
        cur.close()

def delete_all_tables(conn):
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cur.fetchall()
    for table in tables:
        table_name = table[0]
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
    conn.commit()

if __name__ == "__main__":
    try:
        conn = sqlite3.connect("database.db")
    except sqlite3.Error as err:
        print(err)
    else:
        delete_all_tables(conn)
        create_user_table(conn)
        create_cart_table(conn)
        create_products_table(conn)
        create_orders_table(conn)
        add_user(conn, "johndoe", generate_password_hash("Joe123"))
        add_user(conn, "maryjane", generate_password_hash("LoveDogs"))
        add_user(conn, "admin", generate_password_hash("admin123"), "admin")

        insert_product(conn, "Swallow-tailed gull", 12499, "static/src/images/products/seagull.jpg", "Creagrus furcatus",
                       "The swallow-tailed gull has no structural or plumage differences between the male and female. In the breeding season, the adult has a black plumaged head and a bright red fleshy rim around each eye. Outside the breeding season, the head is white and the eye rim becomes black. It has a grayish upper breast, gray mantle, and black wingtips. The mostly black bill has a contrasting white tip.")
        insert_product(conn, "Little gull", 399, "static/src/images/products/seagull1.jpg", "Hydrocoloeus minutus",
                       "This is the smallest gull species, with a length of 25-30 cm (10-12 in), a wingspan of 61-78 cm (24-30+1/2 in), and a mass of 68-162 g (2+3/8-5+3/4 oz). It is pale grey in breeding plumage with a black hood, dark underwings and often a pinkish flush on the breast. In winter, the head goes white apart from a darker cap and eye-spot. The bill is thin and black and the legs dark red. The flight on rounded wings is somewhat tern-like.")
        insert_product(conn, "Ross's gull", 899, "static/src/images/products/seagull2.jpg", "Rhodostethia rosea",
                       "This small bird is similar in size and some plumage characteristics to the little gull. It is slightly larger and longer winged than the little gull species, and has more-pointed wings and a wedge-shaped tail. Its legs are red. Summer adults are pale grey above and white below, with a pink flush to the breast, and a neat black neck ring. In winter, the breast tints and neck collar are lost and a small dark crescent develops behind the eye. Young birds resemble winter adults, but have a dark 'W' pattern on the wings in flight, like young little gulls. The juveniles take two years to attain full adult plumage. Ross's gull measurements:")
        insert_product(conn, "Sabine's gull", 999, "static/src/images/products/seagull3.jpg",
                       "Xema sabini", "The Sabine's gull is a small gull, 27 to 33 cm (10+1/2-13 in) in length and weighing 135 to 225 g (4+3/4-7+15/16 oz). The wings are long, thin and pointed with a span of between 81 and 87 cm (32-34+1/2 in). The bill, which is black with a yellow tip, is around 2.5 cm (1 in) long. This species is easy to identify through its striking wing pattern. The adult has a pale grey back and wing coverts, black primary flight feathers and white secondaries. The white tail is forked. The male's hood darkens during breeding season. Young birds have a similar tricoloured wing pattern, but the grey is replaced by brown, and the tail has a black terminal band. Juveniles take two years to attain full adult plumage. Sabine's gulls have an unusual molt pattern for gulls. Fledged birds retain their juvenile plumage through the autumn and do not start molting into their first winter plumage until they have reached their wintering grounds. Adults have their complete molt in the spring prior to the spring migration, and have a partial molt in the autumn after returning to the wintering area, a reversal of the usual pattern for gulls. They have a very high-pitched and squeaking call.")
        insert_product(conn, "Ivory gull", 3999, "static/src/images/products/seagull4.jpg", "Pagophila eburnea",
                       "This species is easy to identify. At approximately 43 centimetres (17 in), it has a different, more pigeon-like shape than the Larus gulls, but the adult has completely white plumage, lacking the grey back of other gulls. The thick bill is blue with a yellow tip, and the legs are black. The bill is tipped with red, and the eyes have a fleshy, bright red eye-ring in the breeding season. Its flight call cry is a harsh, tern-like keeeer. It has many other vocalizations, including a warbling 'fox-call' that indicates potential predators such as an Arctic fox, polar bear, Glaucous Gull or human near a nest, a 'long-call' given with wrists out, elongated neck and downward-pointed bill, given in elaborate display to other Ivories during breeding, and a plaintive begging call. given in courtship by females to males, accompanied by head-tossing. Young birds have a dusky face and variable amounts of black flecking in the wings and tail. The juveniles take two years to attain full adult plumage. There are no differences in appearance across the species' geographic range.")
        insert_product(conn, "Saunder's gull", 19999, "static/src/images/products/seagull5.jpg", "Chroicocephalus saundersi",
                       "This is a very small species of gull with a length of just 33 cm (13 in) and, among gulls, only the little gull is smaller. Adults have a black hood and nape during the breeding season. It is very pale with a white body, pale grey wings and a narrow black tail band. The legs and short bill are black and the body is squat. Non-breeding birds have a mottled grey hood and nape, and white-tipped wings with black markings on the primaries.")
        insert_product(conn, "Pacific gull", 599, "static/src/images/products/seagull6.jpg", "Larus pacificus",
                       "Pacific gulls are the only large gulls in their range, besides the occasional kelp gull. This species can range in length from 58 to 66 cm (23 to 26 in) and span 137 to 157 cm (54 to 62 in) across the wings. They typically weigh from 900 to 1,180 g (1.98 to 2.60 lb). This species is mostly white, with dark wings and back, and a very thick (when compared to other gull species), powerful, red-tipped yellow bill. They have salt glands that secrete salty water through the nostrils. Young birds are mottled-brown all over, and attain their adult plumage only gradually; by its fourth year, a young Pacific gull has usually become difficult to tell apart from an adult bird. Of the two subspecies, the nominate eastern race prefers sheltered beaches, and the western race L. p. georgii is commonly found even on exposed shores. Both subspecies nest in pairs or loose colonies on offshore islands, making a cup of grasses and sticks in an exposed position, and laying two or three mottled brown eggs.")
        insert_product(conn, "Belcher's gull", 499, "static/src/images/products/seagull7.jpg", "Larus belcheri",
                       "Belcher's gull grows to a length of about 49 centimetres (19 in). The sexes are similar in appearance and in the breeding season, the adult has a white head and very pale grey neck and underparts. The mantle and back are greyish-black and the tail is white with a broad black subterminal band and a white trailing edge. The wing coverts and primaries are black and the secondaries dark grey with white tips. The eye is black, the bill yellow with a distinctive red and black tip, and the legs and feet yellow. Outside the breeding season the head is dark brown with a white ring surrounding the eye. The juvenile is mottled brown and white and attains the adult plumage during its third year. Belcher's gull can be confused with the slightly larger kelp gull (Larus dominicanus) but that species has a small white tip on its otherwise black wing and lacks the Belcher's gull's black band on its tail")
        insert_product(conn, "Olrog's gull", 499, "static/src/images/products/seagull8.jpg", "Larus atlanticus",
                       "Olrog's gull is a large gull with a white head, neck, rump, breast, and belly. The back and wings are black except for a white trailing edge to the wings. The tail is white with a broad black band at the back. The beak is yellow with a black band and red tip. The eyes are brown with a red orbital ring and the legs and feet are dull yellow. The length of this gull is 50 to 60 cm (20 to 24 in) and it has a wingspan of 130 to 140 cm (51 to 55 in). Males are a little larger than females. Juveniles have black heads and brownish plumage.")
        insert_product(conn, "Black-tailed gull", 599, "static/src/images/products/seagull9.jpg", "Larus crassirostris",
                       "The black-tailed gull is medium-sized (46 cm) (19 Inches), with a wingspan of 126-128 cm (49.6 - 50.3 Inches). It has yellow legs and a red and black spot at the end of the bill. Males and females have identical plumage and features, although males are larger in size than females. This gull takes four years to reach full adult plumage. As the name suggests, it has a black tail. The bird has a cat-like call, giving it its Japanese name — umineko (海猫, 'sea cat'), and Korean name — gwaeng-yi gull, which means 'cat' gull. In Hachinohe they are one of the 100 Soundscapes of Japan.")
        insert_product(conn, "Heermann's gull", 4299, "static/src/images/products/seagull10.jpg", "Larus heermanni",
                       "This species looks distinctly different from other gulls. Adults have a medium gray body, blackish-gray wings and tail with white edges, and a red bill with a black tip. The head is dusky gray in non-breeding plumage and white in breeding plumage. Immatures resemble non-breeding adults but are darker and browner, and the bill is pink till the second winter. A few birds, no more than 1 in 200, have white primary coverts, which form a showy spot on the upper wing. This gull is unlikely to be confused with other species as it is the only white-headed, gray-bodied gull found on the west coast of North America.")
        insert_product(conn, "Common gull", 399, "static/src/images/products/seagull11.jpg", "Larus canus",
                       "Adult common gulls are 40-46 cm (16-18 in) long, noticeably smaller than the herring gull and slightly smaller than the ring-billed gull. It is further distinguished from the ring-billed gull by its shorter, more tapered bill, which is a more greenish shade of yellow and is unmarked during the breeding season. The body is grey above and white below. The legs are yellow in breeding season, becoming duller in the winter. In winter, the head is streaked grey and the bill often has a poorly defined blackish band near the tip, which is sometimes sufficiently obvious to cause confusion with ring-billed gull. They have black wingtips with large white 'mirrors' on the outer primaries p9 and p10, which are smaller than those in the short-billed gull. Young birds have scaly black-brown upperparts and a neat wing pattern, and pink legs which become greyish in the second year before tuning yellow. By the first winter, the head and belly are white, with fine streaks and greyish feathers grow on the saddle. They take three years (up to four in the Kamchatka subspecies) to reach maturity. The call is a high-pitched 'laughing' cry.")
        insert_product(conn, "Short-billed gull", 599, "static/src/images/products/seagull12.jpg", "Larus brachyrhynchus",
                       "The short-billed gull is a small gull with a length 40-45 cm (16-18 in) and a wingspan 100-120 cm (39-47 in). It is smaller than other gulls in the Common gull complex, with a shorter bill and longer wings. Its wings appear long and narrow in flight relative to its short body. In breeding plumage, adults have a white head, pale eyes surrounded by a red orbital skin, yellow legs and bill with no markings. In winter, the head is marked with brown mottling, the eye orbital skin becomes greyish and the bill becomes duller with a faint dark marking. In flight, the two outermost primary feathers (p9 and p10) have conspicuous white spots or 'mirrors'. Between p5 and p8, the primaries have white 'tongue tips' which form a 'string of pearls' transitioning to the broad white trailing edge. p4 usually has a black markings in many birds. In comparison, common gulls have a larger bill and shorter wings. The wingtips of common gulls have more extensive black wingtips with smaller mirrors on p9-10, a narrower trailing edge, and typically lack black markings on p4 as well as the white tongue tip on p8.")
        insert_product(conn, "Ring-billed gull", 999, "static/src/images/products/seagull13.jpg", "Larus delawarensis",
                       "The head, neck and underparts are white; the relatively short bill is yellow with a dark ring; the back and wings are silver gray; and the legs are yellow. The eyes are yellow with red rims. This gull takes three years to reach its breeding plumage; its appearance changes with each fall moult. The average lifespan of an individual that reaches adulthood is 10.9 years The oldest ring-billed gull on record was observed in Cleveland in 2021, still alive at the age of 28 years.")
        insert_product(conn, "California gull", 799, "static/src/images/products/seagull14.jpg", "Larus californicus",
                       "Adults are similar in appearance to the herring gull, but have a smaller yellow bill with a black ring, yellow legs, brown eyes and a more rounded head. The body is mainly white with grey back and upper wings. They have black primaries with white tips. Immature birds are also similar in appearance to immature herring gulls, with browner plumage than immature ring-billed gulls. Length can range from 46 to 55 cm (18 to 22 in), the wingspan 122-137 cm (48-54 in) and body mass can vary from 430 to 1,045 g (0.948 to 2.304 lb).")
        insert_product(conn, "Great black-backed gull", 2999, "static/src/images/products/seagull15.jpg", "Larus marinus",
                       "This is the largest gull in the world, considerably larger than a herring gull (Larus argentatus). Only a few other gulls, including Pallas's gull (Ichthyaetus ichthyaetus) and glaucous gull (Larus hyperboreus), come close to matching this species' size. It is 64-79 cm (25-31 in) long with a 1.5-1.7 m (4 ft 11 in - 5 ft 7 in) wingspan and a body weight of 0.75-2.3 kg (1 lb 10 oz - 5 lb 1 oz). In a sample of 2009 adults from the North Atlantic, males were found to average 1,830 g (4 lb 1/2 oz) and females were found to average 1,488 g (3 lb 4+1/2 oz). Some adult gulls with access to fisheries in the North Sea can weigh up to roughly 2.5 kg (5+1/2 lb) and averaged 1.96 kg (4 lb 5 oz). An exceptionally large glaucous gull was found to outweigh any known great black-backed gull, although usually that species is slightly smaller. The great black-backed gull is bulky and imposing in appearance with a large, powerful bill. The standard measurements are: the bill is 5.4 to 7.25 cm (2+1/8 to 2+7/8 in), the wing chord is 44.5 to 53 cm (17+1/2 to 20+3/4 in) and the tarsus is 6.6 to 8.8 cm (2+5/8 to 3+1/2 in).. The adult great black-backed gull is fairly distinctive, as no other very large gull with blackish coloration on its upper-wings generally occurs in the North Atlantic. In other white-headed North Atlantic gulls, the mantle is generally a lighter gray color and, in some species, it is a light powdery color or even pinkish. It is grayish-black on the wings and back, with conspicuous, contrasting white 'mirrors' at the wing tips. The legs are pinkish, and the bill is yellow or yellow-pink with some orange or red near tip of lower bill. The adult lesser black-backed gull (L. fuscus) is distinctly smaller, typically weighing about half as much as a great black-back. The lesser black-back has yellowish legs and a mantle that can range from slate-gray to brownish-colored but it is never as dark as the larger species. A few superficially similar dark-backed, fairly large gulls occur in the Pacific Ocean or in the tropics, all generally far outside this species' range, such as the slaty-backed (L. schistisagus), the western (L. occidentalis) and the kelp gull (L. dominicanus).Juvenile birds of under a year old have scaly, checkered black-brown upper parts, the head and underparts streaked with gray brown, and a neat wing pattern. The face and nape are paler and the wing flight feathers are blackish-brown. The juvenile's tail is white with zigzag bars and spots at base and a broken blackish band near the tip. The bill of the juvenile is brownish-black with white tip and the legs dark bluish-gray with some pink tones. As the young gull ages, the gray-brown coloration gradually fades to more contrasting plumage and the bill darkens to black before growing paler. By the third year, the young gulls resemble a streakier, dirtier-looking version of the adult. They take at least four years to reach maturity, development in this species being somewhat slower than that of other large gulls. The call is a deep 'laughing' cry, kaa-ga-ga, with the first note sometimes drawn out in an almost bovid-like sound. The voice is distinctly deeper than most other gull species.")
        insert_product(conn, "Kelp gull", 399, "static/src/images/products/seagull16.jpg", "Larus dominicanus",
                       "The kelp gull superficially resembles two gulls from further north in the Atlantic Ocean, the lesser black-backed gull and the great black-backed gull and is intermediate in size between these two species. This species ranges from 54 to 65 cm (21 to 26 in) in total length, from 128 to 142 cm (50 to 56 in) in wingspan and from 540 to 1,390 g (1.19 to 3.06 lb) in weight. Adult males and females weigh on average 1,000 g (2.2 lb) and 900 g (2.0 lb) respectively. Among standard measurements, the wing chord is 37.3 to 44.8 cm (14.7 to 17.6 in), the bill is 4.4 to 5.9 cm (1.7 to 2.3 in) and the tarsus is 5.3 to 7.5 cm (2.1 to 3.0 in). The adult kelp gull has black upper parts and wings. The head, underparts, tail, and the small 'mirrors' at the wing tips are white. The bill is yellow with a red spot, and the legs are greenish-yellow (brighter and yellower when breeding, duller and greener when not breeding). The call is a strident ki-och. Juveniles have dull legs, a black bill, a dark band in the tail, and an overall grey-brown plumage densely edged whitish, but they rapidly get a pale base to the bill and largely white head and underparts. They take three or four years to reach maturity.")
        insert_product(conn, "Glaucous-winged gull", 899, "static/src/images/products/seagull17.jpg", "Larus glaucescens",
                       "This gull is a large bird, being close in size and shape to the closely related Western gull (L. occidentalis). It measures 50-68 cm (20-27 in) in length and 120-150 cm (47-59 in) in wingspan, with a body mass of 730-1,690 g (1.61-3.73 lb). It weighs around 1,010 g (2.23 lb) on average. Among standard measurements, the wing chord is 39.2 to 48 cm (15.4 to 18.9 in), the bill is 4.6 to 6.4 cm (1.8 to 2.5 in) and the tarsus is 5.8 to 7.8 cm (2.3 to 3.1 in). It has a white head, neck, breast, and belly, a white tail. The silver-gray wings and back form the mantle, which is darker than that of the Glaucous gull and paler than the Herring gull and Western Gull. The primary flight feathers (wingtips) are grey, usually the same shade as the mantle. Its legs are pink and the beak is yellow with a red subterminal spot (the spot near the end of the bill that chicks peck in order to stimulate regurgitative feeding). The irises are typically dark, and surrounded by pink orbital skin. The forehead is somewhat flat. During the winter, the head and nape is darker with a varied smudged or mottled pattern, and the bill colour becomes duller, often with dark markings near the tip. Young birds are brown or gray with black beaks, and take four years to reach adult plumage.")
        insert_product(conn, "Western gull", 799, "static/src/images/products/seagull18.jpg", "Larus occidentalis",
                       "The western gull is a large gull that can measure 55 to 68 cm (22 to 27 in) in total length, spans 130 to 144 cm (51 to 57 in) across the wings, and weighs 800 to 1,400 g (1.8 to 3.1 lb). The average mass among a survey of 48 gulls of the species was 1,011 g (2.229 lb). Among standard measurements, the wing chord is 38 to 44.8 cm (15.0 to 17.6 in), the bill is 4.7 to 6.2 cm (1.9 to 2.4 in) and the tarsus is 5.8 to 7.5 cm (2.3 to 3.0 in). The western gull has a white head and body, and upperparts or mantle is dark grey. The head generally remains white year-round, developing little to no streaking in northern populations. It has a large and bulbous-tipped yellow bill with a red subterminal spot (this is the small spot near the end of the bill that chicks peck in order to stimulate feeding). The eye colour varies, averaging pale yellow in southern populations and darker in northern populations. It closely resembles the slaty-backed gull (Larus schistisagus) of Asia, but the latter species has paler eyes and deeper pink legs and eye orbitals. In the north of its range it forms a hybrid zone with its close relative the glaucous-winged gull (Larus glaucescens). Western gulls take approximately four years to reach their full plumage, their layer of feathers and the patterns and colors on the feathers. In adult plumage, The largest western gull colony is on the Farallon Islands, located about 26 mi (40 km) west of San Francisco, California; an estimated 30,000 gulls live in the San Francisco Bay area. Western gulls also live in the Oregon Coast.Two subspecies are recognized, differentiated by the mantle and eye colouration. The northern subspecies L. o. occidentalis is found between Central Washington and Central California, has dark grey upperparts. The southern subspecies L. o. wymani is found between central and southern California has a darker mantle (approaching that of the Great black-backed gull) and has paler eyes on average. wymani has more advanced plumage development than occidentalis, and generally attains adult plumage by the third year.")
        insert_product(conn, "Yellow-footed gull", 499, "static/src/images/products/seagull19.jpg", "Larus livens",
                       "Adults are similar in appearance to the western gull with a white head, dark, slate-colored back and wings, and a thick yellow bill. Its legs are yellow, though first winter birds do display pink legs like those of the western gull. It attains full plumage at three years of age. This species is tied with slaty-backed gull for the world's fourth-largest gull species and is one of the largest gulls in the world, being slightly larger than the western gull. It measures 53 to 72 cm (21 to 28 in) in length and spans 140 to 160 cm (55 to 63 in) across the wings. The body mass of this species can vary from 930 to 1,500 g (2.05 to 3.31 lb). Among standard measurements, the wing chord is 40 to 46 cm (16 to 18 in), the bill is 5.0 to 6.2 cm (2.0 to 2.4 in) and the tarsus is 5.9 to 7.5 cm (2.3 to 3.0 in).")
        insert_product(conn, "Glaucous gull", 1599, "static/src/images/products/seagull20.jpg", "Larus hyperboreus",
                       "This is a large and powerful gull, second-largest of all gull species and very pale in all plumage, with no black on either the wings or the tail. Adults are pale grey above, with a thick, yellow bill. Juveniles are very pale grey with a pink and black bill. This species is considerably larger, bulkier, and thicker-billed than the similar Iceland gull, and can sometimes equal the size of the great black-backed gull, the oft-titled largest gull species. In some areas, glaucous gulls are about the same weight as great black-backed gulls or even heavier, and their maximum weight is greater. They can weigh from 960 to 2,700 g (2.12 to 5.95 lb), with the sexes previously reported to average 1.55 kg (3.4 lb) in males and 1.35 kg (3.0 lb) in females. At the colony on Coats Island in Canada, the gulls are nearly 15% heavier than some other known populations, with a mean weight 1.86 kg (4.1 lb) in five males and 1.49 kg (3.3 lb) in seven females. One other study claimed even higher weights for glaucous gulls, as on Wrangel Island, 9 males reportedly averaged 2.32 kg (5.1 lb) and 2.1 kg (4.6 lb) in six females, which if accurate, would make the glaucous gull the heaviest gull and shorebird in the world if not (as far as is known) the largest in length on average. These gulls range from 55 to 77 cm (22 to 30 in) in length and can span 132 to 170 cm (52 to 67 in), with some specimens possibly attaining 182 cm (72 in), across the wings. Among standard measurements, the wing chord is 40.8 to 50.1 cm (16.1 to 19.7 in), the bill is 4.9 to 6.9 cm (1.9 to 2.7 in) and the tarsus is 6 to 7.7 cm (2.4 to 3.0 in). They take four years to reach maturity. The call is a 'laughing' cry similar to that of the herring gull, but deeper.")
        insert_product(conn, "Iceland gull", 799, "static/src/images/products/seagull21.jpg", "Larus glaucoides",
                       "The Iceland gull is a medium-sized gull, although relatively slender and light in weight. In length, it can measure from 50 to 64 cm (20 to 25 in), wingspan is from 115 to 150 cm (45 to 59 in), and weight is from 480 to 1,100 g (1.06 to 2.43 lb). Among standard measurements, the wing chord is 37.9 to 44.3 cm (14.9 to 17.4 in), the bill is 3.6 to 5.4 cm (1.4 to 2.1 in), and the tarsus is 4.9 to 6.7 cm (1.9 to 2.6 in). It is smaller and thinner-billed than the very large glaucous gull, and is usually smaller than the herring gull. It takes four years to reach maturity.")
        insert_product(conn, "European herring gull", 99, "static/src/images/products/seagull22.jpg", "Larus argentatus",
                       "The male European herring gull is 60-67 cm (24-26 in) long and weighs 1,050-1,525 g (2.315-3.362 lb), while the female is 55-62 cm (22-24 in) and weighs 710-1,100 g (1.57-2.43 lb). The wingspan can range from 125 to 155 cm (49 to 61 in). Among standard measurements, the wing chord is 38 to 48 cm (15 to 19 in), the bill is 4.4 to 6.5 cm (1.7 to 2.6 in) and the tarsus is 5.3 to 7.5 cm (2.1 to 3.0 in). Adults in breeding plumage have a light grey back and upper wings and white head and underparts. The wingtips are black with white spots known as 'mirrors'. The bill is yellow with a red spot and a ring of bare yellow skin is seen around the pale eye. The legs are normally pink at all ages, but can be yellowish, particularly in the Baltic population, which was formerly regarded as a separate subspecies 'L. a. omissus'. Non-breeding adults have brown streaks on their heads and necks. Male and female plumage are identical at all stages of development, but adult males are often larger. Juvenile and first-winter birds are mainly brown with darker streaks and have a dark bill and eyes. Second-winter birds have a whiter head and underparts with less streaking and the back is grey. Third-winter individuals are similar to adults, but retain some of the features of immature birds such as brown feathers in the wings and dark markings on the bill. The European herring gull attains adult plumage and reaches sexual maturity at an average age of four years.")
        insert_product(conn, "American herring gull", 199, "static/src/images/products/seagull23.jpg", "Larus smithsonianus",
                       "It is a heavily built large gull with a long powerful bill, full chest and sloping forehead. Males are 60-66 cm (24-26 in) long and weigh 1,050-1,650 g (2.31-3.64 lb). Females are 53-62 cm (21-24 in) long and weigh 600-900 g (1.3-2.0 lb). The wingspan is 120 to 155 cm (47 to 61 in). Among standard measurements, the wing chord is 41.2 to 46.8 cm (16.2 to 18.4 in), the bill is 4.4 to 6.2 cm (1.7 to 2.4 in) and the tarsus is 5.5 to 7.6 cm (2.2 to 3.0 in). Breeding adults have a white head, rump, tail, and underparts and a pale gray back and upperwings. The wingtips are black with white spots known as 'mirrors' and the trailing edge of the wing is white. The underwing is grayish with dark tips to the outer primary feathers. The legs and feet are normally pink but can have a bluish tinge, or occasionally be yellow. The bill is yellow with a red spot on the lower mandible. The eye is bright, pale to medium yellow, with a bare yellow or orange ring around it. In winter, the head and neck are streaked with brown. Young birds take four years to reach fully adult plumage. During this time they go through several plumage stages and can be very variable in appearance. First-winter birds are gray-brown with a dark tail, a brown rump with dark bars, dark outer primaries and pale inner primaries, dark eyes, and a dark bill, which usually develops a paler base through the winter. The head is often paler than the body. Second-winter birds typically have a pale eye, pale bill with black tip, pale head and begin to show gray feathers on the back. Third-winter birds are closer to adults but still have some black on the bill and brown on the body and wings and have a black band on the tail.")
        insert_product(conn, "Yellow-legged gull", 799, "static/src/images/products/seagull24.jpg", "Larus michahellis",
                       "The yellow-legged gull is a large gull, though the size does vary, with the smallest females being scarcely larger than a common gull and the largest males being roughly the size of a great black-backed gull. They range in length from 52 to 68 cm (20 to 27 in) in total length, from 120 to 155 cm (47 to 61 in) in wingspan and from 550 to 1,600 g (1.21 to 3.53 lb) in weight. Among standard measurements, the wing chord is 40.8 to 47.2 cm (16.1 to 18.6 in), the bill is 4.6 to 6 cm (1.8 to 2.4 in) and the tarsus is 5.6 to 7.5 cm (2.2 to 3.0 in). Adults are externally similar to herring gulls but have yellow legs. They have a grey back, slightly darker than herring gulls but lighter than lesser black-backed gulls. They are much whiter-headed in autumn, and have more extensively black wing tips with few white spots, just as lesser black-backed. They have a red spot on the bill as adults, like the entire complex. There is a red ring around the eye like in the lesser black-backed gull but unlike in the herring gull which has a dark yellow ring. First-year birds have a paler head, rump and underparts than those of the herring gull, more closely resembling first-year great black-backed gulls in plumage. They have a dark bill and eyes, pinkish grey legs, dark flight feathers and a well-defined black band on the tail. They become lighter in the underparts and lose the upperpart pattern subsequently. By their second winter, birds are essentially feathered like adults, save for the patterned feathers remaining on the wing coverts. However, their bill tips are black, their eyes still dark, and the legs are a light yellow flesh colour. The call is a loud laugh which is deeper and more nasal than the call of the herring gull.")
        insert_product(conn, "Caspian gull", 499, "static/src/images/products/seagull25.jpg", "Larus cachinnans",
                       "It is a large gull at 56-68 cm (22-27 in) long, with a 137 to 155 cm (54 to 61 in) wingspan and a body mass of 680-1,590 g (1.50-3.51 lb). Among standard measurements, the wing chord is 38.5 to 48 cm (15.2 to 18.9 in), the bill is 4.6 to 6.4 cm (1.8 to 2.5 in) and the tarsus is 5.8 to 7.7 cm (2.3 to 3.0 in). The Caspian gull has a long, slender bill, accentuated by the sloping forehead. The legs, wings, and neck are longer than those of the herring gull and yellow-legged gull. The eye is small and often dark, and the legs vary from pale pink to a pale yellowish colour. The back and wings are a slightly darker shade of grey than the herring gull, but slightly paler than the yellow-legged gull. The outermost primary feather has a large white tip and a white tongue running up the inner web. First-winter birds have a pale head with dark streaking on the back of the neck. The underparts are pale and the back is greyish. The greater and median wing coverts have whitish tips forming two pale lines across the wing.")
        insert_product(conn, "Vega gull", 499, "static/src/images/products/seagull26.jpg", "Larus vegae",
                       "The Vega gull is similar to the herring gull but is slightly darker grey above. The head of the Vega gull is heavily streaked with brown in winter, especially on the back and sides of the neck forming a collar. The legs are usually bright pink. First- and second-winter Vega gulls are darker than the similar Mongolian gull, notably on the crown of the head where Mongolian gulls even in first- and second-winter are a bit paler. Almost the full body of first- and second-winter Vega gulls displays darker brown flecks and streaks. Adult Vega gulls in winter can often be mistaken for the very similar-looking slaty-backed gull (L. schistisagus) and the western gull (L. occidentalis), but the Vega gull's gray is lighter than the two similar species. Eye colour is variable but tends to be dark with a red orbital ring. The bill is yellow with a red spot except for first- and second-winter gulls where the bill can be almost entirely dark gray/black, with the gray portion shrinking until it reaches maturity. Vega gulls in the northwestern part of their breeding range are paler above. They are sometimes considered to be a separate subspecies named Birula's gull (Larus vegae birulai)")
        insert_product(conn, "Armenian gull", 699, "static/src/images/products/seagull27.jpg", "Larus armenicus",
                       "The Armenian gull is a fairly large gull species, though it is on average the smallest of the 'herring gull' complex. It can range from 52 to 62 cm (20 to 24 in), from 120 to 145 cm (47 to 57 in) across the wings, and weighs from 600 to 960 g (1.32 to 2.12 lb). Among standard measurements, its wing chord is 38.5 to 45.8 cm (15.2 to 18.0 in), its bill is 4.1 to 5.6 cm (1.6 to 2.2 in) and its tarsus is 5.7 to 6.4 cm (2.2 to 2.5 in). They are superficially similar to yellow-legged gulls but are slightly smaller with a slightly darker grey back and dark eyes. The area of black on the wingtips is more extensive with smaller white spots. The bill is short with a distinctive black band just before the tip. First-winter birds are mainly brown. They have a whitish rump, pale inner primary feathers, and a narrow, sharply-defined black band on the tail. Although their ranges do not overlap, with its darkish mantle, both black and red near the tip of its bill and a dark eye, the Armenian gull bears a remarkable resemblance to the California gull (L. californicus) of North America.")
        insert_product(conn, "Slaty-backed gull", 499, "static/src/images/products/seagull28.jpg", "Larus schistisagus",
                       "It is tied with the yellow-footed gull for fourth-largest gull species, measuring 55-68.5 cm (21.7-27.0 in) in length, 132-160 cm (52-63 in) in wingspan, and 1.05-1.7 kg (2.3-3.7 lb) in weight. Among standard measurements, the wing chord is 40 to 48 cm (16 to 19 in), the bill is 4.8 to 6.5 cm (1.9 to 2.6 in), and the tarsus is 6 to 7.6 cm (2.4 to 3.0 in). It has a white head, belly, and tail with a dark slaty-gray back and wings with a broad white trailing edge. The wings and back are slightly darker than those of the western gull (Kodak grey scale 9.5 to 12 compared to Kodak 9 to 11 of the darker southern subspecies of Western Gull). On the outer primaries (p9 and p10), there are white spots called mirrors. The inner webs to primaries are pale grey, and the mid-primaries have long grey tongues tipped with large white crescents, forming a 'string of pearls' pattern connecting to the broad white trailing edge of the secondaries. Its eyes are yellow surrounded by purple to deep pink orbital skin. The legs are pink and short when compared with those of similar-looking gulls, and the body appears more stout with a 'pot-bellied' appearance. The bill is yellow with orange-red subterminal spot (the spot near the end of the bill that chicks peck to stimulate regurgitative feeding). Immature gulls' plumage is brown, similar to that of the great black-backed gull, but paler, and is practically indistinguishable from the immature herring gull in the field.")
        insert_product(conn, "Lesser black-backed gull", 399, "static/src/images/products/seagull29.jpg", "Larus fuscus",
                       "The lesser black-backed gull is smaller than the European herring gull. The taxonomy of the herring gull / lesser black-backed gull complex is very complicated; different authorities recognise between two and eight species. This group has a ring species distribution around the Northern Hemisphere. Differences between adjacent forms in this ring are fairly small, but by the time the circuit is completed, the end members, herring gull and lesser black-backed gull, are clearly different species. The lesser black-backed gull measures 51-64 cm (20-25 in), 124-150 cm (49-59 in) across the wings, and weighs 452-1,100 g (0.996-2.425 lb), with the nominate race averaging slightly smaller than the other two subspecies. Males, at an average weight of 824 g (1.817 lb), are slightly larger than females, at an average of 708 g (1.561 lb). Among standard measurements, the wing chord is 38 to 45 cm (15 to 18 in), the bill is 4.2 to 5.8 cm (1.7 to 2.3 in), and the tarsus is 5.2 to 6.9 cm (2.0 to 2.7 in). A confusable species is the great black-backed gull. The lesser is a much smaller bird, with slimmer build, yellow rather than pinkish legs, and smaller white 'mirrors' at the wing tips. The adults have black or dark grey wings (depending on race) and back. The bill is yellow with a red spot at which the young peck, inducing feeding (see fixed action pattern). The head is greyer in winter, unlike great black-backed gulls. Annual moult for adults begins between May and August and is not complete on some birds until November. Partial prebreeding moult occurs between January and April. Young birds have scaly black-brown upperparts and a neat wing pattern. They take four years to reach maturity. Identification from juvenile herring gulls is most readily done by the more solidly dark (unbarred) tertial feathers. Their call is a 'laughing' cry like that of the herring gull, but with a markedly deeper pitch.")
        insert_product(conn, "White-eyed gull", 799, "static/src/images/products/seagull30.jpg", "Ichthyaetus leucophthalmus",
                       "Adult white-eyed gulls have a black hood in breeding plumage, which extends down onto the upper throat, and on the neck-sides is bordered below by a narrow white bar. The upperparts and inner upperwings are medium-dark grey; the breast is mid-grey but the rest of the underparts are white. The secondaries are black with a white trailing edge, and the primaries are black. The underwing is dark and the tail white. Adults in non-breeding plumage are similar, but the hood is flecked white small white spots. The white-eyed gull acquires adult plumage at two to three years of age. Juvenile birds have a very different plumage—chocolate brown on the head, neck and breast, and with brown, broadly pale-fringed, feathers to the upperparts and upperwings, and a black tail. In their first winter, birds acquire greyer feathering on their head, breast and upperparts; the second-winter plumage is closer to that of the adult, but lacking the hood. A distinctive feature of white-eyed gull at all ages is its long slender bill. This is black in younger birds, but in adults it is deep red with a black tip. The legs are yellow—dullest in younger birds, brightest in breeding plumaged adults. The eye itself is not white; the bird takes its name from white eye-crescents, which are present at all ages.")
        insert_product(conn, "pingu", 499, "static/src/images/products/pingu.jpg", "a nice piongu",
                       "Baby Emperor is an adorable, enchanting character that captivates the hearts of both children and adults alike. With a crown of innocence and a smile that radiates pure joy, Baby Emperor embodies the perfect blend of regal charm and innocent curiosity. As the youngest ruler of a whimsical kingdom, Baby Emperor embarks on delightful adventures, spreading laughter and warmth wherever they go. With their endearing clumsiness and boundless imagination, Baby Emperor reminds us of the wonders of childhood, teaching us to cherish the magic in every moment.")
        insert_product(conn, "Sooty gull", 1299, "static/src/images/products/seagull31.jpg", "Ichthyaetus hemprichii",
                       "The sooty gull (Ichthyaetus hemprichii) is a species of gull in the family Laridae, also known as the Aden gull or Hemprich's gull. It is found in Bahrain, Djibouti, Egypt, Eritrea, India, Iran, Israel, Jordan, Kenya, Lebanon, Maldives, Mozambique, Oman, Pakistan, Palestine, Qatar, Saudi Arabia, Somalia, Sri Lanka, Sudan, Tanzania, United Arab Emirates, and Yemen. As is the case with many gulls, it has traditionally been placed in the genus Larus. The sooty gull is named in honour of the German naturalist Wilhelm Hemprich who died in 1825 while on a scientific expedition to Egypt and the Middle East with his friend Christian Gottfried Ehrenberg.")
        insert_product(conn, "Pallas's gull", 999, "static/src/images/products/seagull32.jpg", "Ichthyaetus ichthyaetus",
                       "This is a very large gull, being easily the world's largest black-headed gull and the third largest species of gull in the world, after the great black-backed gull and the glaucous gull. It measures 55-72 cm (22-28 in) in length with a 142 to 170 cm (56 to 67 in) wingspan. Weight can vary from 0.96-2.1 kg (2.1-4.6 lb), with an average of 1.6 kg (3.5 lb) in males and 1.22 kg (2.7 lb) in females. Among standard measurements, the wing chord is 43.5 to 52 cm (17.1 to 20.5 in), the bill is 4.7 to 7.3 cm (1.9 to 2.9 in) and the tarsus is 6.5 to 8.4 cm (2.6 to 3.3 in). Summer adults are unmistakable, since no other gull of this size has a black hood. The adults have grey wings and back, with conspicuous white 'mirrors' at the wing tips. The legs are yellow and the bill is orangey-yellow with a red tip. In all other plumages, a dark mask through the eye indicates the vestiges of the hood. The call is a deep aargh cry. Young birds attain largely grey upperparts quite rapidly, but they take four years to reach maturity.")
        insert_product(conn, "Audouin's gull", 39999, "static/src/images/products/seagull33.jpg", "Ichthyaetus audouinii",
                       "Audouin's gull (Ichthyaetus audouinii) is a large gull restricted to the Mediterranean and the western coast of Saharan Africa and the Iberian Peninsula. The genus name is from Ancient Greek ikhthus, 'fish', and aetos, 'eagle', and the specific audouinii and the English name are after the French naturalist Jean Victoire Audouin. It breeds on small islands colonially or alone, laying 2-3 eggs on a ground nest. As is the case with many gulls, it has traditionally been placed in the genus Larus. In the late 1960s, this was one of the world's rarest gulls, with a population of only 1,000 pairs. It has established new colonies, but remains rare with a population of about 10,000 pairs. This species, unlike many large gulls, rarely scavenges, but is a specialist fish eater, and is therefore strictly coastal and pelagic. This bird will feed at night, often well out to sea, but also slowly patrols close into beaches, occasionally dangling its legs to increase drag. The adult basically resembles a small European herring gull, the most noticeable differences being the short stubby red bill and 'string of pearls' white wing primary tips, rather than the large 'mirrors' of some other species. The legs are grey-green. It takes four years to reach adult plumage. This species shows little tendency to wander from its breeding areas, but there were single records in the Netherlands and England in May 2003, and one spent from December 2016 to April 2017 in Trinidad.")
        insert_product(conn, "Mediterranean gull", 399, "static/src/images/products/seagull34.jpg",
                       "Ichthyaetus melanocephalus", "The Mediterranean gull is slightly larger and bulkier than the black-headed gull with a heavier bill and longer, darker legs. The breeding plumage adult is a distinctive white gull, with a very pale grey mantle and wings with white primary feathers without black tips. The black hood extends down the nape and shows distinct white eye crescents. The sharp-tipped, parallel sided, dark red bill has a black subterminal band. The non breeding adult is similar but the hood is reduced to an extensive dusky 'bandit' mask through the eye. This bird takes two years to reach maturity. First year birds have a black terminal tail band and more black areas in the upperwings, but have pale underwings.")
        insert_product(conn, "Relict gull", 1699, "static/src/images/products/seagull35.jpg",
                       "Ichthyaetus relictus", "The gull is 44 to 45 cm long with a stocky, thick body. Non-breeding adults feature uniformly dark-smudged ear-coverts and hind crown, white-tipped wings, prominent, isolated black subterminal markings on outer primaries, and no white leading edge to outer wing. Breeding birds have black hoods (including napes) with grey-brown foreheads, and broad, white, half-moon colouring behind, below, and above their eyes. Their legs are orange and their bills scarlet. The name comes from its status as a relict species.")
        insert_product(conn, "Seagull", 1499, "static/src/images/products/seagull36.jpg",
                       "A cool gull I found", "I found this gull in my backyard. It might be rare but I don't know.")
        insert_product(conn, "Dolphin gull", 499, "static/src/images/products/seagull37.jpg", "Leucophaeus scoresbii", 
                       "The dolphin gull (Leucophaeus scoresbii), sometimes erroneously called the red-billed gull (a somewhat similar but unrelated species from New Zealand), is a gull native to southern Chile and Argentina, and the Falkland Islands. It is a coastal bird inhabiting rocky, muddy and sandy shores and is often found around seabird colonies. They have greyish feathers, and the feathers on their wings are a darker shade. Dolphin gulls have a varied diet, eating many things ranging from mussels to carrion. The modern scientific name Leucophaeus scoresbii, together with the obsolete common name Scoresby's gull, commemorates the English explorer William Scoresby (1789-1857).")
        insert_product(conn, "Laughing gull", 899, "static/src/images/products/seagull38.jpg", "Leucophaeus atricilla", 
                       "This species is 36-41 cm (14-16 in) long with a 98-110 cm (39-43 in) wingspan and a weight range of 203-371 grams (7.2-13.1 oz). The summer adult's body is white apart from the dark grey back and wings and black head. Its wings are much darker grey than all other gulls of similar size except the smaller Franklin's gull, and they have black tips without the white crescent shown by Franklin's. The beak is long and red. The black hood is mostly lost in winter. Laughing gulls take three years to reach adult plumage. Immature birds are always darker than most similar-sized gulls other than Franklin's. First-year birds are greyer below and have paler heads than first-year Franklin's, and second-years can be distinguished by the wing pattern and structure.")
        insert_product(conn, "Franklin's gull", 399, "static/src/images/products/seagull39.jpg", "Leucophaeus pipixcan", 
                       "It breeds in central provinces of Canada and adjacent states of the northern United States. It is a migratory bird, wintering in Argentina, the Caribbean, Chile, and Peru. The summer adult's body is white and its back and wings are much darker grey than all other gulls of similar size except the larger laughing gull. The wings have black tips with an adjacent white band. The bill and legs are red. The black hood of the breeding adult is mostly lost in winter. Young birds are similar to the adult but have less developed hoods and lack the white wing band. They take three years to reach maturity.")
        insert_product(conn, "Lava gull", 2599, "static/src/images/products/seagull40.jpg", "Leucophaeus fuliginosus", 
                       "The entire population lives on the Galapagos Islands where it is found predominantly on the islands of Santa Cruz, Isabela, San Cristobal and Genovesa. Previously its population was estimated at 300-400 pairs; this estimate was revised downwards to 300-600 individuals in 2015. It is currently considered the rarest gull in the world.")
        insert_product(conn, "Grey gull", 399, "static/src/images/products/seagull41.jpg", "Leucophaeus modestus", 
                       "The sexes are similar in grey gulls. Adults grow to a length of about 45 cm (18 in) and weigh some 360 to 400 g (13 to 14 oz). The head is white in summer but brownish-grey in winter. The body and wings are grey with the dorsal surface rather darker than the ventral region. The flight feathers are black and the inner primaries and the secondaries have white tips, visible in flight. The tail has a band of black with a white trailing edge. The legs and beak are black and the iris is brown. The call is similar to that of the laughing gull (Leucophaeus atricilla).")
        insert_product(conn, "Silver gull", 899, "static/src/images/products/seagull42.jpg", "Chroicocephalus novaehollandiae", 
                       "The head, body, and tail are white. The wings are light grey with white-spotted, black tips. Adults range from 40-45 cm (15-17 Inches) in length. Mean wingspan is 94 cm (37 Inches) . Juveniles have brown patterns on their wings, and a dark beak. Adults have bright red beaks—the brighter the red, the older the bird.")
        insert_product(conn, "Hartlaub's gull", 499, "static/src/images/products/seagull43.jpg", "Chroicocephalus hartlaubii", 
                       "Hartlaub's gull is 36-38 cm in length. It is a mainly white gull with a grey back and upperwings, black wingtips with conspicuous white 'mirrors', and a dark red bill and legs. When breeding it has a very faint lavender grey hood, but otherwise has a plain white head. Sexes are similar. This species differs from the slightly larger grey-headed gull in its thinner, darker bill, deeper red legs, paler, plainer head, and dark eyes. It takes two years to reach maturity. Juvenile birds have a brown band across the wings. They differ from same-age grey-headed gulls in that they lack a black terminal tail band, less dark areas in the wings, darker legs, and a white head.")
        insert_product(conn, "Brown-hooded gull", 699, "static/src/images/products/seagull44.jpg", "Chroicocephalus maculipennis", 
                       "The mature bird has a dark brown head and throat with a white semicircle around the posterior part of the eye, while the neck, chest and abdomen are white. The beak and legs are red. The primary flight feathers are dark gray, while the secondaries and covert feathers are a lighter gray. This bird may be confused with the Franklin's gull. There is no significant sexual dimorphism.")
        insert_product(conn, "Grey-headed gull",1199 , "static/src/images/products/seagull45.jpg", "Chroicocephalus cirrocephalus", 
                       "The grey-headed gull is slightly larger than the black-headed gull at 42 cm length. The summer adult has a pale gray head, a gray body, darker in tone than the black-headed, and red bill and legs. The black tips to the primary wing feathers have conspicuous white 'mirrors'. The underwing is dark gray with black wingtips. The gray hood is lost in winter, leaving just dark streaks. Sexes are similar. The South American race is slightly larger and paler-backed than the African subspecies.")
        insert_product(conn, "Andean gull", 699, "static/src/images/products/seagull46.jpg", "Chroicocephalus serranus", 
                       "The Andean gull is 42 to 48 cm (17 to 19 in) long and weighs about 480 g (17 oz); it is one of the larger members of its genus. The sexes are alike. Adults in breeding plumage have a glossy black hood with a white crescent behind the eye and a mostly white body with a gray back and sometimes a pink flush on the underparts. Their tail is white. The upper side of their wing is mostly gray with an alternating white-black-white-black pattern on the primaries. The underside of their wing is pale gray with a blackish outer half but for large white 'mirrors' on the three outermost primaries. Their bill, legs, and feet are blackish brown with a reddish tinge and their iris is brown. Non-breeding adults have a white head and blackish legs. The Andean gull takes two years to attain adult plumage. In its first year it has some mottled black on its head, a complex black and white pattern on the wings, and a black band near the end of the tail.")
        insert_product(conn, "Black-billed gull", 1199, "static/src/images/products/seagull47.jpg", "Chroicocephalus bulleri", 
                       "A healthy adult black-billed gull is typically 35-38 cm long, with a wingspan of 81-96 cm, and a weight of around 230g.:545 The head, body, and parts of the wings are white, with silvery grey on the saddle and wings, as well as black edging on the wings.:546 The gull also undergoes some seasonal color change. While typically black from February to June, the orbital ring is orange-red, red, or dark red the rest of the year.:556 The legs, too, change from black to dark red and even bright red as the breeding season progresses, 'possibly stimulated by presence of begging chicks and juveniles.':556 Observations suggest the gull is sexually dimorphic, but there is a lack of published data to support this.: 557  There is likewise a lack of data in regard to geographical variation.: 557 ")
        insert_product(conn, "Brown-headed gull", 399, "static/src/images/products/seagull48.jpg", "Chroicocephalus brunnicephalus", 
                       "The brown-headed gull is slightly larger than black-headed gull. The summer adult has a pale brown head, lighter than that of black-headed, a pale grey body, and red bill and legs. The black tips to the primary wing feathers have conspicuous white 'mirrors'. The underwing is grey with black flight feathers. The brown hood is lost in winter, leaving just dark vertical streaks.")
        insert_product(conn, "Black-headed gull", 399, "static/src/images/products/seagull49.jpg", "Chroicocephalus ridibundus", 
                       "This gull is 37-44 cm (14+1/2-17+1/2 in) long with a 94-110 cm (37-43+1/2 in) wingspan and weighs 190-400 g (6+3/4 1+1/8 oz). In flight, the white leading edge to the wing is a good field mark. The summer adult has a chocolate-brown head (not black, although does look black from a distance), pale grey body, black tips to the primary wing feathers, and red bill and legs. The hood is lost in winter, leaving just two dark spots. Immature birds have a mottled pattern of brown spots over most of the body, and a black band on the tail. There is no difference in plumage between the sexes. It breeds in colonies in large reed beds or marshes, or on islands in lakes, nesting on the ground. Like most gulls, it is highly gregarious in winter, both when feeding or in evening roosts. It is not a pelagic species and is rarely seen at sea far from coasts. The black-headed gull is a bold and opportunistic feeder. It eats insects, fish, seeds, worms, scraps, and carrion in towns, or invertebrates in ploughed fields with equal relish. It is a noisy species, especially in colonies, with a familiar 'kree-ar' call. Its scientific name means laughing gull. This species takes two years to reach maturity. First-year birds have a black terminal tail band, more dark areas in the wings, and, in summer, a less fully developed dark hood. Like most gulls, black-headed gulls are long-lived birds, with a maximum age of at least 32.9 years recorded in the wild, in addition to an anecdote now believed of dubious authenticity regarding a 63-year-old bird.")
        insert_product(conn, "Slender-billed gull", 799, "static/src/images/products/seagull50.jpg", "Chroicocephalus genei", 
                       "This species is 37 to 40 cm (14.6 to 15.7 in) long with a 90 to 102 cm (35.4 to 40.2 in) wingspan. It is therefore slightly larger than the black-headed gull, which it resembles, although it does not have a black hood in summer. It has a pale grey body, white head and breast and black tips to the primary wing feathers. The head and dark red bill have an elongated tapering appearance, and this bird also appears long-necked. The legs are dark red, and the iris is yellow. In summer, the breast has a faint pink colouration. This bird takes two years to reach maturity, as is usual in gulls. First year immature birds have a black terminal tail band, and dark areas on the wings.")
        insert_product(conn, "Bonaparte's gull", 699, "static/src/images/products/seagull51.jpg", "Chroicocephalus philadelphia", 
                       "Bonaparte's gull is among the smallest of the gull species; only little gull and Saunders's gull are smaller. Adults range from 28 to 38 cm (11 to 15 in) in length, with a wingspan of 76-84 cm (30-33 in) and a body mass of 180-225 g (6.3-7.9 oz). There is no difference in plumage or bare part colour between the sexes, though males tend to be heavier than females. Bonaparte's gull is smaller-bodied, smaller-headed, and smaller-billed than the other common hooded gulls of North America. The adult has grey upperparts and white underparts; its wingtips are black above and pale below. In breeding plumage, it has a slaty black hood, which it loses in non-breeding plumage. Its short, thin bill is black, and its legs are orangish-red. First year Bonaparte's gulls have the same plumage in winter and summer, but the summer plumage is paler due to wear. Fewer than 5 percent of Bonaparte's gulls acquire a dark hood in their first summer, and on those that do, the hood is duller than on breeding adults.")
        insert_product(conn, "Black-legged kittiwake", 2399, "static/src/images/products/seagull52.jpg", "Rissa tridactyla", 
                       "This gull is 37-41 cm (15-16 in) in length with a wingspan of 91-105 cm (36-41 in) and a body mass of 305-525 g (10.8-18.5 oz). It has a white head and body, grey back, grey wings tipped solid black, black legs and a yellow bill. Occasional individuals have pinky-grey to reddish legs, inviting confusion with red-legged kittiwake. The inside of their mouth is also a characteristic feature of the species due to its rich red colour. Such red pigmentation is due to carotenoids pigments and vitamin A which have to be acquired through their diet. Studies show that integument coloration is associated with male's reproductive success. Such hypothesis would explain the behavior of couples greeting each other by opening their mouth and flashing their bright mouth it to their partner while vocalizing. As their Latin name suggests, they only possess three toes since their hind toe is either extremely reduced or completely absent. The two subspecies being almost identical, R. tridactyla pollicaris is in general slightly larger than its counterpart R. tridactyle tridactyla. In winter, this species acquires a dark grey smudge behind the eye and a grey hind-neck collar. The bill also turns a dusky-olive color. Since kittiwakes winter at sea and rarely touch ground during this period, very little is known about their exact molting pattern.")
        insert_product(conn, "Red-legged kittiwake", 2399, "static/src/images/products/seagull53.jpg", "Rissa brevirostris", 
                       "The red-legged kittiwake is a very localised subarctic Pacific species. Apart from the distinguishing feature implicit in its name, it is very similar to its better known relative, the black-legged kittiwake; other differences include the shorter bill, larger eyes, a larger, rounder head and darker grey wings, and in the juveniles, which barely differ from the adults, lacking the black tail band and 'W' across the wings of juvenile black-legged kittiwakes. Juveniles take three years to reach maturity. Adults are 35-39 cm (14-15 in) long, with an 84-92 cm (33-36 in) wingspan and a body mass of 325-510 g (11.5-18.0 oz). Like the Pacific race of black-legged kittiwake, the red-legged kittiwake has a well-developed hind toe. As occasional individual black-legged kittiwakes have reddish legs, any reports of red-legged away from the subarctic Pacific must record all of the other differences, not just the leg colour, for acceptance by bird recording authorities.")
        hash = get_hash_for_login(conn, "maryjane")
        print("Check password: {}".format(
            check_password_hash(hash, "LoveDogs")))

        conn.close()
