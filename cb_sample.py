import psycopg2
import smtplib
from tabulate import tabulate
from datetime import datetime
from email.message import EmailMessage

try:

    # connect to aws clientboxx db - production instance
    conn = psycopg2.connect(
        database="database",
        user="user",
        password="password",
        host="host",
        port='5432' 
    )

    # START/SETUP
    now = datetime.now()
    dt1_string = now.strftime("%d%m%Y%H%M%S")
    dt2_string = now.strftime("%d/%m/%Y %H:%M")
    fname = "cb_user_report_"+dt1_string+".txt"
    f = open(fname, mode='a')
    f.write("==========================================\n")
    f.write("ClientBoxx Usage Report: "+dt2_string+"\n")
    f.write("==========================================\n\n")
    
    try:
        cur = conn.cursor()
 
        ## NEW USER THIS WEEK LISTING: 
        # execute a query (filter on 30 days for testing)
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(cu.client_id) as \"client count\", extract(day from now()::timestamp - u.created_at::timestamp) as \"account age\" from \"user\" as u, client_user as cu where u.id = cu.user_id and u.email not like '%calc%' and u.email not like '%yopmail%' and u.email not like '%cognitive%' and u.email not like '%aol%' and u.email not like '%ds.com%' and u.email not like '%charlesnem%' and u.email not like '%mordecai%' and u.email not like '%akash%' and u.email not like '%samanth%' and extract(day from now()::timestamp - u.created_at::timestamp) < 30 group by u.id order by u.name")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table     
        f.write("ClientBoxx New Users This Week: "+str(cur.rowcount)+"\n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Client Count","Account Age"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END NEW USER THIS WEEK LISTING

        ## USER LISTING: at some point, this will need to be a weekly filter (new this week)
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(cu.client_id) as \"client count\" from \"user\" as u, client_user as cu where u.id = cu.user_id and u.email not like '%calc%' and u.email not like '%yopmail%' and u.email not like '%cognitive%' and u.email not like '%aol%' and u.email not like '%ds.com%' and u.email not like '%charlesnem%' and u.email not like '%mordecai%' and u.email not like '%akash%' and u.email not like '%samanth%' group by u.id order by u.name")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table     
        f.write("ClientBoxx Users: "+str(cur.rowcount)+"\n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Client Count"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END USER LISTING

        ## STORAGE DETAILS: at some point, this will need to be something like a top 20 storage usage listing (some kind of threshold report)
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(at.id), sum(at.file_size)/1000000000 from \"user\" as u, attachment as at where u.id = at.user_id and u.email not like '%calc%' and u.email not like '%yopmail%' and u.email not like '%cognitive%' and u.email not like '%aol%' and u.email not like '%ds.com%' and u.email not like '%charlesnem%' and u.email not like '%mordecai%' and u.email not like '%akash%' and u.email not like '%samanth%' group by u.id order by u.name")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table     
        f.write("ClientBoxx Storage: \n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Attachment Count","Storage GB"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END STORAGE DETAILS

        ## ATTACHMENT DETAILS: at some point, this will need to be something like a top 20 storage usage listing (some kind of threshold report)
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(at.id) as \"attachment count\", case when cast(at.type as char) like '%1%' then 'doc' when cast(at.type as char) like '%2%' then 'img' when cast(at.type as char) like '%3%' then 'vid' when cast(at.type as char) like '%4%' then 'note' else cast(at.type as char) end as \"type\", sum(at.file_size)/1000000000 as \"storage in GB\" from \"user\" as u, attachment as at where u.id = at.user_id and u.email not like '%calc%' and u.email not like '%yopmail%' and u.email not like '%cognitive%' and u.email not like '%aol%' and u.email not like '%ds.com%' and u.email not like '%charlesnem%' and u.email not like '%mordecai%' and u.email not like '%akash%' and u.email not like '%samanth%' group by u.id, at.type order by u.name,\"attachment count\" desc, \"storage in GB\" desc")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table     
        f.write("ClientBoxx Attachments: \n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Attachment Count","Type","Storage GB"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END STORAGE DETAILS

        ## TOTAL STORAGE
        # execute a query
        cur.execute("select sum(file_size)/1000000000 as \"storage in GB\" from attachment")
        # get the results
        rowStuff = cur.fetchone()
        # tabulate the results into a pretty table     
        # write 'em out
        if rowStuff is not None:
            sumStorage = str(rowStuff[0])
            f.write("ClientBoxx Total Storage: "+str(rowStuff[0])+"\n\n")
        else:
            f.write("** NO DATA **")
        ## END STORAGE DETAILS

        ## SIGNATURE
            f.write("======================================\n")
            f.write("               THE END\n")
            f.write("        (report by python_don)\n")
            f.write("     (pretty tables  by tabulate)\n")
            f.write("(delivered by xxxxxxxxxxxxx@gmail.com)\n")
            f.write("======================================")
        ## END SIGNATURE

    ## CLOSE UP SHOP
    finally:
        f.close()

    # close cursor
    cur.close

    ## EMAIL THE FILE TO CI PEEPS
    gmail_user = 'user'
    gmail_password = 'password'
    cbreport = fname 
    sender = 'sender'
    receivers = ['receivers']

    msg = EmailMessage()
    msg["From"] = sender
    msg["Subject"] = "weekly clientboxx usage"
    msg["To"] = receivers
    msg.set_content("GTB'ers,\n\nPlease see attached weekly ClientBoxx usage report.\n\nNote: If you see a GB Storage value like \"5e-08\", it is because the user only has Notes attachment types which has no file size; postgresql returns junk, sorry.\n\nThanks,\nDon")
    msg.add_attachment(open(cbreport, "r").read(), filename=cbreport)

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sender, receivers, msg.as_string())
        server.close()         
        print("Successfully sent email")
    except smtplib.SMTPException:
        print("Error: unable to send email")

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()