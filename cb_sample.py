import sqlite3
from tabulate import tabulate
from datetime import datetime

try:

    # connect to clientboxx db - local test instance
    conn = sqlite3.connect('cbdb.db')

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
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(cu.client_id) as \"client count\", julianday('now') - julianday(u.created_at) as \"account age\" from \"user\" as u, client_user as cu where u.id = cu.user_id and julianday('now') - julianday(u.created_at) < 30 group by u.id order by u.name")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table   
        f.write("ClientBoxx New Users This Week: "+str(len(rowStuff))+"\n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Client Count","Account Age"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END NEW USER THIS WEEK LISTING

        ## USER LISTING
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(cu.client_id) as \"client count\" from \"user\" as u, client_user as cu where u.id = cu.user_id group by u.id order by u.name")
        # get the results
        rowStuff = cur.fetchall()
        # tabulate the results into a pretty table     
        f.write("ClientBoxx Users: "+str(len(rowStuff))+"\n")
        # write 'em out
        if rowStuff is not None:
            f.write(tabulate(rowStuff, headers=["ID","Name","Email","Phone","Created On","Client Count"],tablefmt='fancy_grid'))
            f.write("\n\n")
        else:
            f.write("** NO DATA **")
        ## END USER LISTING

        ## STORAGE DETAILS
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(at.id), round(sum(at.file_size)/1000000000,2) from \"user\" as u, attachment as at where u.id = at.user_id group by u.id order by u.name")
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

        ## ATTACHMENT DETAILS
        # execute a query
        cur.execute("select distinct u.id, u.name, u.email, u.phone, u.created_at, count(at.id) as \"attachment count\", case when cast(at.type as char) like '%1%' then 'doc' when cast(at.type as char) like '%2%' then 'img' when cast(at.type as char) like '%3%' then 'vid' when cast(at.type as char) like '%4%' then 'note' else cast(at.type as char) end as \"type\", round(sum(at.file_size)/1000000000,2) as \"storage in GB\" from \"user\" as u, attachment as at where u.id = at.user_id group by u.id, at.type order by u.name,\"attachment count\" desc, \"storage in GB\" desc")
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
        cur.execute("select round(sum(file_size)/1000000000,2) as \"storage in GB\" from attachment")
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
            f.write("        (report by <yourname here>)\n")
            f.write("     (pretty tables  by tabulate)\n")
            f.write("(delivered by xxxx@emaildomainhere.com)\n")
            f.write("======================================")
        ## END SIGNATURE

    ## CLOSE UP SHOP
    finally:
        f.close()

    # close cursor
    cur.close()

except (Exception, psycopg2.DatabaseError) as error:
    print(error)

finally:
    if conn is not None:
        conn.close()
