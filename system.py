try:
    from tkinter import *
    from tkinter.messagebox import *
    import sqlite3
    from traceback import print_tb
    from dataconn import *

    root = Tk()

    systitle = '用户注册信息管理系统'
    root.title(systitle)
    curWidth, curHeight = 651, 432
    scnWidth, scnHeight = root.maxsize()
    geocnf = '%dx%d+%d+%d' % (curWidth, curHeight,(scnWidth - curWidth) / 2, (scnHeight - curHeight) / 2)
    root.geometry(geocnf)

    photo = PhotoImage(file='image/background.png')
    # imglabel = Label(image = photo)
    # imglabel.place(x=0, y=0)
    a = Label(root,text='欢迎使用\n用户管理系统',image = photo, compound=CENTER, fg='white', font=('微软雅黑', 30)).place(x=0, y=0)

    mainframe = LabelFrame()
    mainframe.pack()

    logfile = 'user_management_error.log'

    def adminlogin():
        global mainframe
        mainframe.destroy()
        mainframe = LabelFrame(text='管理员登录')
        mainframe.pack(anchor=CENTER, pady=80, ipadx=10, ipady=10)

        def totxtpassword(event):
            txtpassword.focus()

        def tobtnlogin(event):
            btnlogin.focus()

        def test(content):
            if content.isdigt() or content == "":
                return True
            else:
                return False
        test_cmd =root.register(test)

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
        txtpassword.bind('<Return>', tobtnlogin)

        frmbottom = Frame(mainframe)
        frmbottom.pack(pady=5)
        btnlogin = Button(frmbottom, text='登录')
        btnlogin.config(width=8, activeforeground='red')
        btnlogin.grid(row=1, column=3)

        def check(username,password):
            value = [username, password]
            conn = getconn()
            cur = conn.cursor()
            cur.execute('select * from admin where username = %s and password = %s ', value)
            users = cur.fetchall()
            conn.close()
            if len(users) > 0:
                return True
            else:
                return False

        def login():
            username = txtusername.get ()
            password = txtpassword.get()
            if check(username, password):
                showinfo(systitle, '输入正确！点击确定进入管理员界面')
                root.destroy()
                import admin
            else:
                showerror(systitle, '账号或密码输入错误!')

        btnlogin.config(command=login)

    def studentlogin():
        import stu_login

    def schoollogin():
        pass

    def thirdlogin():
        pass

    def exit():
        if askokcancel(systitle, '你要退出系统吗？'):
            root.destroy()

    menubar = Menu(root)
    root.config(menu=menubar)
    file = Menu(menubar, tearoff=0)
    file.add_command(label='管理员登录', command=adminlogin)
    file.add_separator()
    file.add_command(label='学生登录', command=studentlogin)
    file.add_command(label='院校登录', command=schoollogin)
    file.add_command(label='第三方登录', command=thirdlogin)
    file.add_separator()
    file.add_command(label='退出系统', command=exit)
    menubar.add_cascade(label='系统操作', menu=file)

    mainloop()

except Exception as ex:
    log = open(logfile, 'a')
    print('异常信息：', ex)
