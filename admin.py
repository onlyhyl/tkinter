try:
    from tkinter.messagebox import *
    from tkinter import *
    from dataconn import *

    root = Tk()

    systitle = '用户注册信息管理系统'
    root.title(systitle)
    curWidth, curHeight = 651, 365
    scnWidth, scnHeight = root.maxsize()
    geocnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
    root.geometry(geocnf)

    photo = PhotoImage(file='image/admin_bg.png ')
    # imglabel = Label(image = photo)
    # imglabel.place(x=0, y=0)
    a = Label(root, text='欢迎使用\n管理员系统', image=photo, compound=CENTER, fg='white', font=('微软雅黑', 30)).place(x=0, y=0)

    logfile = 'user_management_error.log'
    mainframe = LabelFrame()
    mainframe.pack()


    # 用户管理
    def stdfind(username):
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from std where username = "%s" ' % username)
        users = cur.fetchall()
        conn.close()
        if len(users) > 0:
            return True
        else:
            return False

    def adminfind(username):
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from admin where username = "%s" ' % username)
        users = cur.fetchall()
        conn.close()
        if len(users) > 0:
            return True
        else:
            return False

    def adduser():
        global mainframe
        mainframe.destroy()
        mainframe = LabelFrame(text='添加新用户')
        mainframe.pack(anchor=CENTER, pady=80, ipadx=10, ipady=10)

        def totxtpassword(event):
            txtpassword.focus()

        def tobtnsave(event):
            btnsave.focus()

        def test(content):
            if content.isdigt() or content == "":
                return True
            else:
                return False

        test_cmd = root.register(test)

        frmtop = Frame(mainframe)
        frmtop.pack()

        Label(frmtop, text='用户名:', anchor=E).grid(row=1, column=1)
        username = StringVar()
        txtusername = Entry(frmtop, textvariable=username, )
        txtusername.grid(row=1, column=2)
        txtusername.bind('<Return>', totxtpassword)
        txtusername.focus()

        Label(frmtop, text='密 码：', anchor=E).grid(row=2, column=1)
        password = StringVar()
        txtpassword = Entry(frmtop, textvariable=password, show='*')
        txtpassword.grid(row=2, column=2)
        txtpassword.bind('<Return>', tobtnsave)

        frmrad = Frame(mainframe)
        frmrad.pack(pady=2)
        v = IntVar()
        r1 = Radiobutton(frmrad, text="管理员", variable=v, value=1).pack()
        r2 = Radiobutton(frmrad, text="学生", variable=v, value=2).pack()

        frmbottom = Frame(mainframe)
        frmbottom.pack(pady=5)
        btnsave = Button(frmbottom, text='保存')
        btnsave.config(width=8, activeforeground='red')
        btnsave.grid(row=2, column=1)
        btnclear = Button(frmbottom, text='重置')
        btnclear.config(width=8, activeforeground='red')
        btnclear.grid(row=2, column=2)

        def save():

            def adminsave():
                username = txtusername.get()
                password = txtpassword.get()
                if username == '':
                    showerror(systitle, '用户名不能为空')
                else:
                    if adminfind(username):
                        showerror(systitle, '用户名已存在，重新输入用户名')
                        txtusername.focus()
                        txtusername.select_range(0, END)
                    else:
                        if password == '':
                            showerror(systitle, '密码不能为空！')
                            txtpassword.focus()
                        else:
                            conn = getconn()
                            cur = conn.cursor()
                            cur.execute('insert into admin values ("%s","%s")' % (username, password))
                            conn.commit()
                            conn.close()
                            showinfo(systitle, '管理员：[' + username + ']添加成功！')

            def stdsave():
                username = txtusername.get()
                password = txtpassword.get()
                if username == '':
                    showerror(systitle, '用户名不能为空')
                else:
                    if stdfind(username):
                        showerror(systitle, '用户名已存在，重新输入用户名')
                        txtusername.focus()
                        txtusername.select_range(0, END)
                    else:
                        if password == '':
                            showerror(systitle, '密码不能为空！')
                            txtpassword.focus()
                        else:
                            conn = getconn()
                            cur = conn.cursor()
                            cur.execute('insert into std values ("%s","%s")' % (username, password))
                            conn.commit()
                            conn.close()
                            showinfo(systitle, '学生：[' + username + ']添加成功！')

            if v.get() == 1:
                adminsave()
            elif v.get() == 2:
                stdsave()

        def clear():
            username.set('')
            password.set('')
            txtusername.focus()

        btnsave.config(command=save)
        btnclear.config(command=clear)

    def showall():
        global mainframe
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from std')
        users = cur.fetchall()
        conn.close()
        mainframe.destroy()
        if len(users) == 0:
            showwarning(systitle, '当前没有学生注册用户！')
        else:
            mainframe = LabelFrame(text='学生用户')
            mainframe.pack(anchor=CENTER, padx=5, pady=5, ipadx=5, ipady=5)
            mainframe.columnconfigure(1, minsize=80)
            mainframe.columnconfigure(2, minsize=200)
            mainframe.columnconfigure(3, minsize=200)
            Label(mainframe, text='序号', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=1, sticky=N + E + S + W)
            Label(mainframe, text='用户名', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=2, sticky=N + E + S + W)
            Label(mainframe, text='密码', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=3, sticky=N + E + S + W)
            rn = 2  # 行号
            for user in users:
                cn = 1  # 列号
                Label(mainframe, text=str(rn - 1), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=cn, sticky=N + E + S + W)
                for field in user:
                    cn = cn + 1
                    Label(mainframe, text=str(field), font=('宋体', 12), bd=1,
                          relief=SOLID).grid(row=rn, column=cn, sticky=N + E + S + W)
                rn = rn + 1

    # def resetdb():
    #     global mainframe
    #     mainframe.destroy()
    #     msg = '将删除全部注册用户！\n请你确认是否要继续？'
    #     if askokcancel(systitle, msg):
    #         import os
    #         if os.path.exists(dbfile):
    #             os.remove(dbfile)
    #             showinfo(systitle, '系统重置数据库！')
    #         else:
    #             showinfo(systitle, '系统创建数据库！')
    #         conn = getconn()
    #         conn.execute('create table user(username text primary key, password text)')
    #         conn.close()

    def check_update():
        global mainframe
        mainframe.destroy()

        mainframe = LabelFrame(text='查找、修改或删除用户', width=400, height=300)
        mainframe.pack(anchor=CENTER, pady=20, ipadx=5, ipady=5)

        findframe = LabelFrame(mainframe, text='查找用户')
        findframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        Label(findframe, text='输入待查用户名：', anchor=E).grid(row=1, column=1)
        username = StringVar()
        txtusername = Entry(findframe, textvariable=username)
        txtusername.grid(row=1, column=2)
        txtusername.focus()
        btnfind = Button(findframe, text='查找')
        btnfind.grid(row=1, column=3)

        deleteframe = LabelFrame(mainframe, text='删除用户')
        deleteframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        btndelete = Button(deleteframe, text='删除用户', state=DISABLED)
        btndelete.pack(fill=X, padx=10)

        editframe = LabelFrame(mainframe, text='修改用户')
        editframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        Label(editframe, text='新用户名：').grid(row=1, column=1)
        newusername = StringVar()
        txtnewusername = Entry(editframe, textvariable=newusername)
        txtnewusername.grid(row=1, column=2)
        Label(editframe, text='新 密 码：').grid(row=2, column=1)
        newpassword = StringVar()
        txtnewpassword = Entry(editframe, textvariable=newpassword, show='*')
        txtnewpassword.grid(row=2, column=2)
        btnupdate = Button(editframe, text='更新用户信息', state=DISABLED)
        btnupdate.grid(row=1, column=3, rowspan=2, sticky=N + S)

        def finduser():
            username = txtusername.get()
            if not stdfind(username):
                showinfo(systitle, '[%s]还未注册！' % username)
            else:
                btndelete.config(state=NORMAL)
                btnupdate.config(state=NORMAL)

        def deleteuser():
            username = txtusername.get()
            if askyesno(systitle, '要删除用户[%s]吗？' % username):
                conn = getconn()
                cur = conn.cursor()
                cur.execute('delete from std where username = "%s"' % username)
                conn.commit()
                conn.close()
                showinfo(systitle, '成功删除用户[%s]！' % username)
                txtusername.delete(0, END)
                btndelete.config(state=DISABLED)
                btnupdate.config(state=DISABLED)

        def updateuser():
            username = txtusername.get()
            newusername = txtnewusername.get()
            if newusername == '':
                showerror(systitle, '新用户名不能为空！')
                txtnewusername.focus()
            else:
                if stdfind(newusername):
                    showerror(systitle, '用户名[%s]已经注过册！' % newusername)
                    txtnewusername.focus()
                else:
                    newpassword = txtnewpassword.get()
                    if newpassword == '':
                        showerror(systitle, '密码不能为空！')
                    else:
                        conn = getconn()
                        cur = conn.cursor()
                        cur.execute('update std set username = "%s", password = "%s" where username = "%s"' % (
                        newusername, newpassword, username))
                        conn.commit()
                        conn.close()
                        showinfo(systitle, '用户数据更新成功！')

        btnfind.config(command=finduser)
        btndelete.config(command=deleteuser)
        btnupdate.config(command=updateuser)


    # 信息管理
    def stdmsfind(number):
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from stdms where number = "%s" ' % number)
        users = cur.fetchall()
        conn.close()
        if len(users) > 0:
            return True
        else:
            return False

    def addstd():
        global mainframe
        mainframe.destroy()
        mainframe = LabelFrame(text='添加学生信息')
        mainframe.pack(anchor=N, pady=30, ipadx=10, ipady=10)

        def totxtsex(event):
            txtsex.focus()

        def totxtschool(event):
            txtschool.focus()

        def totxtgrade(event):
            txtgrade.focus()

        def totxtnumber(event):
            txtnumber.focus()

        def totxtdepartment(event):
            txtdepartment.focus()

        def totxtbirthdate(event):
            txtbirthdate.focus()

        def totxtendate(event):
            txtendate.focus()

        def totxthome(event):
            txthome.focus()

        def tobtnsave(event):
            btnsave.focus()

        def test(content):
            if content.isdigt() or content == "":
                return True
            else:
                return False

        test_cmd = root.register(test)

        frmtop = Frame(mainframe)
        frmtop.pack()

        Label(frmtop, text='姓名:', anchor=E).grid(row=1, column=1)
        name = StringVar()
        txtname = Entry(frmtop, textvariable=name)
        txtname.grid(row=1, column=2)
        txtname.bind('<Return>', totxtsex)
        txtname.focus()

        Label(frmtop, text='性别：', anchor=E).grid(row=2, column=1)
        sex = StringVar()
        txtsex = Entry(frmtop, textvariable=sex)
        txtsex.grid(row=2, column=2)
        txtsex.bind('<Return>', totxtschool)

        Label(frmtop, text='学校：', anchor=E).grid(row=3, column=1)
        school = StringVar()
        txtschool = Entry(frmtop, textvariable=school)
        txtschool.grid(row=3, column=2)
        txtschool.bind('<Return>', totxtgrade)

        Label(frmtop, text='年级：', anchor=E).grid(row=4, column=1)
        grade = StringVar()
        txtgrade = Entry(frmtop, textvariable=grade)
        txtgrade.grid(row=4, column=2)
        txtgrade.bind('<Return>', totxtgrade)

        Label(frmtop, text='学号：', anchor=E).grid(row=5, column=1)
        number = StringVar()
        txtnumber = Entry(frmtop, textvariable=number)
        txtnumber.grid(row=5, column=2)
        txtnumber.bind('<Return>', totxtdepartment)

        Label(frmtop, text='专业：', anchor=E).grid(row=6, column=1)
        department = StringVar()
        txtdepartment = Entry(frmtop, textvariable=department)
        txtdepartment.grid(row=6, column=2)
        txtdepartment.bind('<Return>', totxtbirthdate)

        Label(frmtop, text='出生日期：', anchor=E).grid(row=7, column=1)
        birthdate = StringVar()
        txtbirthdate = Entry(frmtop, textvariable=birthdate)
        txtbirthdate.grid(row=7, column=2)
        txtbirthdate.bind('<Return>', totxtendate)

        Label(frmtop, text='入学日期：', anchor=E).grid(row=8, column=1)
        endate = StringVar()
        txtendate = Entry(frmtop, textvariable=endate)
        txtendate.grid(row=8, column=2)
        txtendate.bind('<Return>', totxthome)

        Label(frmtop, text='家庭住址：', anchor=E).grid(row=9, column=1)
        home = StringVar()
        txthome = Entry(frmtop, textvariable=home)
        txthome.grid(row=9, column=2)
        txthome.bind('<Return>', tobtnsave)

        frmbottom = Frame(mainframe)
        frmbottom.pack(pady=5)
        btnsave = Button(frmbottom, text='保存')
        btnsave.config(width=8, activeforeground='red')
        btnsave.grid(row=10, column=1)
        btnclear = Button(frmbottom, text='重置')
        btnclear.config(width=8, activeforeground='red')
        btnclear.grid(row=10, column=2)

        def save():
            name = txtname.get()
            sex = txtsex.get()
            school = txtschool.get()
            grade = txtgrade.get()
            number = txtnumber.get()
            department = txtdepartment.get()
            birthdate = txtbirthdate.get()
            endate = txtendate.get()
            home = txthome.get()

            if name == '' and school == '' and grade == '' and number == '' and department == '' and endate == '':
                showerror(systitle, '用户名不能为空')
            else:
                if stdmsfind(number):
                    showerror(systitle, '该学号已存在，重新输入学号')
                    txtnumber.focus()
                    txtnumber.select_range(0, END)
                else:
                    conn = getconn()
                    cur = conn.cursor()
                    cur.execute('insert into stdms values ("%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (name, sex, school, grade, number, department, birthdate, endate, home))
                    conn.commit()
                    conn.close()
                    showinfo(systitle, '学生：[' + name + ']添加成功！')

        def clear():
            name.set('')
            sex.set('')
            school.set('')
            grade.set('')
            number.set('')
            department.set('')
            birthdate.set('')
            endate.set('')
            home.set('')
            txtname.focus()

        btnsave.config(command=save)
        btnclear.config(command=clear)

    def stdfind_ms(name):
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from stdms where name = "%s" ' % name)
        users = cur.fetchall()
        conn.close()
        if len(users) > 0:
            return True
        else:
            return False

    def showall_std():
        global mainframe
        conn = getconn()
        cur = conn.cursor()
        cur.execute('select * from stdms')
        users = cur.fetchall()
        conn.close()
        mainframe.destroy()
        if len(users) == 0:
            showwarning(systitle, '当前没有学生注册信息！')
        else:
            mainframe = LabelFrame(text='学生信息')
            mainframe.pack(anchor=CENTER, padx=5, pady=5, ipadx=5, ipady=5)
            mainframe.columnconfigure(1, minsize=30)
            mainframe.columnconfigure(2, minsize=30)
            mainframe.columnconfigure(3, minsize=50)
            mainframe.columnconfigure(4, minsize=50)
            mainframe.columnconfigure(5, minsize=30)
            mainframe.columnconfigure(6, minsize=50)
            mainframe.columnconfigure(7, minsize=40)
            mainframe.columnconfigure(8, minsize=80)
            mainframe.columnconfigure(9, minsize=80)
            mainframe.columnconfigure(10, minsize=100)
            Label(mainframe, text='序号', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=1, sticky=N + E + S + W)
            Label(mainframe, text='姓名', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=2, sticky=N + E + S + W)
            Label(mainframe, text='性别', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=3, sticky=N + E + S + W)
            Label(mainframe, text='学校', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=4, sticky=N + E + S + W)
            Label(mainframe, text='年级', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=5, sticky=N + E + S + W)
            Label(mainframe, text='学号', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=6, sticky=N + E + S + W)
            Label(mainframe, text='专业', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=7, sticky=N + E + S + W)
            Label(mainframe, text='出生日期', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=8, sticky=N + E + S + W)
            Label(mainframe, text='入学日期', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=9, sticky=N + E + S + W)
            Label(mainframe, text='家庭住址', font=('宋体', 12, 'bold'),
                  bd=1, relief=SOLID).grid(row=1, column=10, sticky=N + E + S + W)
            rn = 2  # 行号
            for user in users:
                cn = 1  # 列号
                Label(mainframe, text=str(rn - 1), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=cn, sticky=N + E + S + W)
                for field in user:
                    cn = cn + 1
                    Label(mainframe, text=str(field), font=('宋体', 12), bd=1,
                          relief=SOLID).grid(row=rn, column=cn, sticky=N + E + S + W)
                rn = rn + 1

    def check_upstd():
        global mainframe
        mainframe.destroy()

        mainframe = LabelFrame(text='查找、修改或删除学生信息', width=400, height=300)
        mainframe.pack(anchor=CENTER, pady=20, ipadx=5, ipady=5)

        findframe = LabelFrame(mainframe, text='查找学生信息')
        findframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        Label(findframe, text='输入待查学生名字：', anchor=E).grid(row=1, column=1)

        findframe.columnconfigure(1, minsize=30)
        findframe.columnconfigure(2, minsize=30)
        findframe.columnconfigure(3, minsize=50)
        findframe.columnconfigure(4, minsize=30)
        findframe.columnconfigure(5, minsize=40)
        Label(findframe, text='姓名', font=('宋体', 12, 'bold'),
              bd=1, relief=SOLID).grid(row=2, column=1, sticky=N + E + S + W)
        Label(findframe, text='学号', font=('宋体', 12, 'bold'),
              bd=1, relief=SOLID).grid(row=2, column=2, sticky=N + E + S + W)
        Label(findframe, text='学校', font=('宋体', 12, 'bold'),
              bd=1, relief=SOLID).grid(row=2, column=3, sticky=N + E + S + W)
        Label(findframe, text='年级', font=('宋体', 12, 'bold'),
              bd=1, relief=SOLID).grid(row=2, column=4, sticky=N + E + S + W)
        Label(findframe, text='专业', font=('宋体', 12, 'bold'),
              bd=1, relief=SOLID).grid(row=2, column=5, sticky=N + E + S + W)

        name = StringVar()
        txtname = Entry(findframe, textvariable=name)
        txtname.grid(row=1, column=2)
        txtname.focus()
        btnfind = Button(findframe, text='查找')
        btnfind.grid(row=1, column=3)

        deleteframe = LabelFrame(mainframe, text='删除学生信息')
        deleteframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        btndelete = Button(deleteframe, text='删除学生信息', state=DISABLED)
        btndelete.pack(fill=X, padx=10)

        editframe = LabelFrame(mainframe, text='修改学生信息')
        editframe.pack(anchor=CENTER, padx=10, ipadx=5, ipady=5, fill=X)
        Label(editframe, text='新姓名：').grid(row=1, column=1)
        newname = StringVar()
        txtnewname = Entry(editframe, textvariable=newname)
        txtnewname.grid(row=1, column=2)
        Label(editframe, text='新学号：').grid(row=2, column=1)
        newnumber = StringVar()
        txtnewnumber = Entry(editframe, textvariable=newnumber)
        txtnewnumber.grid(row=2, column=2)
        Label(editframe, text='新学校：').grid(row=3, column=1)
        newschool = StringVar()
        txtnewschool = Entry(editframe, textvariable=newschool)
        txtnewschool.grid(row=3, column=2)
        Label(editframe, text='新年级：').grid(row=4, column=1)
        newgrade = StringVar()
        txtnewgrade = Entry(editframe, textvariable=newgrade)
        txtnewgrade.grid(row=4, column=2)
        Label(editframe, text='新专业：').grid(row=5, column=1)
        newdepartment = StringVar()
        txtnewdepartment = Entry(editframe, textvariable=newdepartment)
        txtnewdepartment.grid(row=5, column=2)
        btnupdate = Button(editframe, text='更新学生信息', state=DISABLED)
        btnupdate.grid(row=1, column=3, rowspan=2, sticky=N + S)

        def finduser():
            name = txtname.get()
            if not stdfind_ms(name):
                showinfo(systitle, '[%s]还未注册！' % name)
            else:
                conn = getconn()
                cur = conn.cursor()
                cur.execute('select * from stdms where name = "%s" ' % name)
                user = cur.fetchone()
                conn.close()
                rn = 3  # 行号
                # for user in users:
                #     if name in user:
                #         cn = 0  # 列号
                # for field in user:
                # cn = cn + 1
                Label(findframe, text=str(user[0]), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=1, sticky=N + E + S + W)
                Label(findframe, text=str(user[4]), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=2, sticky=N + E + S + W)
                Label(findframe, text=str(user[2]), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=3, sticky=N + E + S + W)
                Label(findframe, text=str(user[3]), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=4, sticky=N + E + S + W)
                Label(findframe, text=str(user[5]), font=('宋体', 12), bd=1,
                      relief=SOLID).grid(row=rn, column=5, sticky=N + E + S + W)
                # rn = rn + 1
                btndelete.config(state=NORMAL)
                btnupdate.config(state=NORMAL)

        def deleteuser():
            name = txtname.get()
            if askyesno(systitle, '要删除学生[%s]信息吗？' % name):
                conn = getconn()
                cur = conn.cursor()
                cur.execute('delete from stdms where name = "%s"' % name)
                conn.commit()
                conn.close()
                showinfo(systitle, '成功删除[%s]信息！' % name)
                txtname.delete(0, END)
                btndelete.config(state=DISABLED)
                btnupdate.config(state=DISABLED)

        def updateuser():
            name = txtname.get()
            newname = txtnewname.get()
            newnumber = txtnewnumber.get()
            newschool = txtnewschool.get()
            newgrade = txtnewgrade.get()
            newdepartment = txtnewdepartment.get()
            if newnumber == '':
                showerror(systitle, '学号不能为空！')
                txtnewnumber.focus()
            else:
                if stdfind(newnumber):
                    showerror(systitle, '学号[%s]已经注过册！' % newnumber)
                    txtnewnumber.focus()
                else:
                    newschool = txtnewschool.get()
                    if newschool == '':
                        showerror(systitle, '学校不能为空！')
                    else:
                        conn = getconn()
                        cur = conn.cursor()
                        cur.execute(
                            'update stdms set name = "%s", number = "%s", school = "%s", grade = "%s", department = "%s" where name = "%s"' % (
                            newname, newnumber, newschool, newgrade, newdepartment, name))
                        conn.commit()
                        conn.close()
                        showinfo(systitle, '学生信息数据更新成功！')

        btnfind.config(command=finduser)
        btndelete.config(command=deleteuser)
        btnupdate.config(command=updateuser)


    # 退出系统
    def exit():
        if askokcancel(systitle, '你要退出管理员系统吗？'):
            root.destroy()


    menubar = Menu(root)
    root.config(menu=menubar)

    file = Menu(menubar, tearoff=0)
    # file.add_command(label='创建/重置用户数据库', command=resetdb)
    file.add_separator()
    file.add_command(label='添加新用户', command=adduser)
    file.add_command(label='显示全部注册用户', command=showall)
    file.add_command(label='查找/修改/删除用户', command=check_update)
    file.add_separator()
    file.add_command(label='退出系统', command=exit)
    menubar.add_cascade(label='用户管理', menu=file)

    file = Menu(menubar, tearoff=0)
    file.add_separator()
    file.add_command(label='添加学生信息', command=addstd)
    file.add_command(label='展示所有学生信息', command=showall_std)
    file.add_command(label='查找/修改/删除学生', command=check_upstd)
    file.add_separator()
    file.add_command(label='添加院校信息')
    file.add_command(label='展示院校信息(含课程等)')
    file.add_command(label='查找/修改/删除院校')
    file.add_separator()
    file.add_command(label='添加第三方机构信息')
    file.add_command(label='展示推荐学生信息')
    file.add_command(label='展示院校及学生评估信息')
    file.add_command(label='查找/修改/删除机构')
    file.add_separator()

    menubar.add_cascade(label='信息管理', menu=file)

except Exception as ex:

    print('异常信息：', ex)
