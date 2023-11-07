import uuid
import psycopg2
import datetime
from weasyprint import HTML, CSS
from jinja2 import Environment, FileSystemLoader


# jinja template configuration
environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("template.html")

# postgres database configuration
connection = psycopg2.connect("dbname=Transaction user=postgres password=qwe@32487")
cur = connection.cursor()

purchase_info = {}

print("Hello Welcome to Pdf Invoice Generator")
opreration_type = input("Do you want to generate Invoice for a new purchase Y/N?\n")

if opreration_type == "N":
    tracking_id = int(input("please enter purchase tracking id"))
    # sql query to get purchase details
    cur.execute("SELECT * FROM purchase WHERE tracking_id = (%s)", (tracking_id,))
    purchase = cur.fetchone()

    purchase_info["id"] = purchase[0]
    purchase_info["tracking_id"] = purchase[1]
    purchase_info["pymanet_date"] = purchase[2]
    purchase_info["payment_mehtod"] = purchase[3]

    # sql query to get purchase products
    cur.execute(
        """SELECT product.name, product.price FROM purchase AS p
            INNER JOIN intermidate_purchase_table as inter_table ON inter_table.purchase_id = p.id 
            INNER JOIN product AS product ON product.id = inter_table.product_id WHERE p.tracking_id = (%s)""",
        (tracking_id,),
    )
    products = cur.fetchall()

    purchase_info["products"] = []
    for i in range(len(products)):
        purchase_info["products"].append((products[i][0], products[i][1]))

    connection.close()

elif opreration_type == "Y":
    purchase_info["purchase_date"] = datetime.date.today().strftime("%Y-%m-%d")

    purchase_method = input("please enter purchase method: \ncash  \ninstallment\n ")
    purchase_method.lower()
    while purchase_method not in {"cash", "Installment"}:
        purchase_method = input(
            "purchase method not available\n available methods: \ncash \ninstallment "
        )
    purchase_info["purchase_method"] = purchase_method

    # generate random number for tracking id
    tracking_id = uuid.uuid4().clock_seq
    purchase_info["tracking_id"] = tracking_id

    cur.execute(
        "INSERT INTO purchase (tracking_id, purchase_method) VALUES (%s,%s)"
        " RETURNING id",
        (
            tracking_id,
            purchase_method,
        ),
    )
    purchase_id = cur.fetchone()[0]
    connection.commit()

    number_of_products = int(input("number of products: "))

    print("first enter the name and the then price of the product")
    purchase_info["products"] = []
    purchase_info["total_price"] = 0

    for i in range(number_of_products):
        product_name = input("product name: ")
        produt_price = float(input("produt price: "))
        purchase_info["total_price"] += produt_price
        purchase_info["products"].append((product_name, produt_price))

        cur.execute(
            "INSERT into product (name, price) VALUES (%s,%s) RETURNING id",
            (
                product_name,
                produt_price,
            ),
        )
        product_id = cur.fetchone()[0]
        connection.commit()

        cur.execute(
            "INSERT INTO intermidate_purchase_table (purchase_id, product_id) VALUES"
            " (%s,%s)",
            (
                purchase_id,
                product_id,
            ),
        )
        connection.commit()
    connection.close()

renderd_tmeplate = template.render(purchase_info)
with open("templates/renderd_template.html", mode="w") as tmeplate_file:
    tmeplate_file.write(renderd_tmeplate)

html = HTML("templates/renderd_template.html")
css = CSS("static/style.css")


pdf_file = open("mypdf.pdf", "w").close()
html.write_pdf("mypdf.pdf", stylesheets=[css])
