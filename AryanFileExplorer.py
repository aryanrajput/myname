from tkinter import *
from tkinter import messagebox
import os
import shutil
from math import floor

class AryanFileExplorer(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.parent = parent;
        self.initilize()

    def initilize(self):
        self.pathvalue = [];
        self.forwordvalue = [];
        self.img = Image("photo", file="AryanED.png")
        menubar = Menu(self);
        filemenu = Menu(menubar, tearoff=0);
        filemenu.add_command(label="New file", command=self.newfile);
        filemenu.add_command(label="New folder", command=self.newfolder);
        filemenu.add_separator();
        filemenu.add_command(label="Exit");
        menubar.add_cascade(label="File", menu=filemenu);
        homebtn = Menu(menubar, tearoff=0);
        homebtn.add_command(label="Copy");
        homebtn.add_command(label="Paste");
        homebtn.add_command(label="Cut");
        homebtn.add_command(label="Delete");
        homebtn.add_command(label="Move");
        homebtn.add_command(label="Rename");
        menubar.add_cascade(label="Home", menu=homebtn);
        view = Menu(menubar, tearoff=0);
        view.add_command(label="Sort By");
        view.add_command(label="item hide");
        menubar.add_cascade(label="View", menu=view);
        helpmenu = Menu(menubar, tearoff=0);
        helpmenu.add_command(label="About AFE");
        helpmenu.add_command(label="Feedback")
        menubar.add_cascade(label="Help", menu=helpmenu);
        self.config(menu=menubar);

        self.refreshimage = PhotoImage(file="refresh.gif");
        self.trashimage = PhotoImage(file="trash.gif");
        self.cutimage = PhotoImage(file="cut.png");
        self.copyimage = PhotoImage(file="copy.png");
        self.selectallimage = PhotoImage(file="selectall.png");
        self.cutimage = PhotoImage(file="cut.png");
        self.newimage = PhotoImage(file="new.png");
        self.newfolderimage = PhotoImage(file="newfolder.png");
        self.renameimage = PhotoImage(file="rename.png");
        self.sortbyimage = PhotoImage(file="sortby.png");

        pw = PanedWindow(self, bg="white", height=40, width=950)
        pw.grid(padx=25, pady=5, sticky=W + E + N + S, columnspan=50, rowspan=5, row=0, column=1);
        tools = PanedWindow(self, borderwidth=8, height=80, width=950);
        tools.grid(padx=25, pady=5, sticky=W + E + N + S, columnspan=50, rowspan=5, row=5, column=1);
        proj = PanedWindow(self, borderwidth=3, bg="white", height=480, width=200, relief=FLAT);
        proj.grid(padx=25, sticky=W, columnspan=10, rowspan=35, row=10, column=1);
        self.propertypanel = Frame(self, bg="white", relief=FLAT, height=85, width=200,);
        self.propertypanel.grid(sticky=S, row=35, column=1,rowspan=40, columnspan=10, pady=10);
        editer = PanedWindow(self, borderwidth=3, bg="white", height=560, width=725)
        editer.grid(padx=25, sticky=W + E + N + S, columnspan=40, rowspan=40, row=11, column=11)

        self.dirpath = Entry(pw, relief=FLAT, width=120);
        self.dirpath.insert(END, os.getcwd())
        pw.add(self.dirpath);
        self.dirpath.bind('<Return>', self.contents)
        pathok = Button(pw, relief=FLAT, width=3, text="ok", command=self.contents)
        pw.add(pathok)
        self.chdirt = StringVar();
        refreshbtn = Button(pw, relief=GROOVE, width=20, bg="#ca3421", text="Refresh",image=self.refreshimage, command=self.contents)
        pw.add(refreshbtn);
        self.searchitem = Entry(pw, bg="gray90", fg="gray50", highlightcolor="white");
        self.searchitem.insert(END, "Search");
        self.searchitem.bind('<FocusIn>', self.entrysearch);
        pw.add(self.searchitem)

        self.back = Button(tools, text="<", relief=GROOVE, fg="black", font="bold", command=self.chdirback);
        tools.add(self.back, pady=21);
        self.forword = Button(tools, text=">", relief=GROOVE, fg="gray", font="bold", command=self.chdirfor);
        tools.add(self.forword, pady=21);
        self.Newfile = Button(tools, text="New", relief=GROOVE, bg="#f5f6f7", image=self.newimage,command=self.newfile);
        tools.add(self.Newfile);
        self.Newfolder = Button(tools, text="New folder", image=self.newfolderimage,relief=GROOVE, bg="#f5f6f7", command=self.newfolder);
        tools.add(self.Newfolder);
        self.openbtn = Button(tools, text="Open", relief=GROOVE, bg="#f5f6f7", state=DISABLED, command=self.open);
        tools.add(self.openbtn);
        self.cut = Button(tools, text="Cut", relief=GROOVE, bg="#f5f6f7",image=self.cutimage, state=DISABLED);
        tools.add(self.cut, pady=10);
        self.copy = Button(tools, text="Copy", relief=GROOVE, bg="#f5f6f7", image=self.copyimage,state=DISABLED);
        tools.add(self.copy);
        self.paste = Button(tools, text="Paste", relief=GROOVE, bg="#f5f6f7", state=DISABLED);
        tools.add(self.paste);
        self.rename = Button(tools, text="Rename", relief=GROOVE, bg="#f5f6f7",image=self.renameimage,state=DISABLED, command=self.rename);
        tools.add(self.rename);
        self.delete = Button(tools, width=40,text="Delete", relief=GROOVE, bg="#f5f6f7",state=DISABLED,image=self.trashimage, command=self.deletefile);
        tools.add(self.delete);
        self.selectall = Button(tools,text="Select all", relief=GROOVE, bg="#f5f6f7", image=self.selectallimage,command=self.selectalllist);
        tools.add(self.selectall, pady=10);
        self.sortby = Button(tools, text="Sort by", relief=GROOVE,image=self.sortbyimage, bg="#f5f6f7");
        tools.add(self.sortby);
        self.itemhide = Button(tools, text="Item hide", relief=GROOVE, bg="#f5f6f7", state=DISABLED);
        tools.add(self.itemhide, pady=10);
        self.aboutme = Button(tools, text="About Developers", relief=GROOVE, bg="lightgray", command=self.aboutjitendar);
        tools.add(self.aboutme);

        self.contextmenu = Menu(self, tearoff=0);
        self.contextmenu.add_command(label="Open", command=self.open);
        self.contextmenu.add_command(label="Refresh", command=self.contents);
        self.submenu = Menu(self, tearoff=0);
        self.submenu.add_command(label="Bluetooth devics");
        self.submenu.add_command(label="Desktop Shortcut");
        self.submenu.add_command(label="Ducument");
        self.submenu.add_command(label="Zip Folder");
        self.submenu.add_command(label="Mail Attachment");
        self.submenu.add_command(label="DVD RW Drive(G:)");
        self.contextmenu.add_command(label="Send to");
        self.contextmenu.add_cascade(label="Send To", menu=self.submenu)
        self.contextmenu.add_command(label="Cut");
        self.contextmenu.add_command(label="Copy");
        self.contextmenu.add_command(label="Paste");
        self.contextmenu.add_command(label="Delete", command=self.deletefile);
        self.contextmenu.add_command(label="Rename", command=self.rename);
        self.newmenu = Menu(self, tearoff=0);
        self.newmenu.add_command(label="New", command=self.newfile);
        self.newmenu.add_command(label="New folder", command=self.newfolder);
        self.contextmenu.add_cascade(label="New", menu=self.newmenu)
        self.contextmenu.add_separator();
        self.contextmenu.add_command(label="Property");


        self.scrollme = Scrollbar(editer);
        self.listbox = Listbox(editer, width=116, yscrollcommand=self.scrollme.set, selectmode=EXTENDED);
        self.itemno = 0;
        self.item = sorted(os.listdir(str(os.getcwd())));
        while(self.itemno<len(self.item)):
            self.listbox.insert(self.itemno, self.item[self.itemno]);
            self.itemno+=1;

        editer.add(self.listbox);
        self.listbox.bind("<<ListboxSelect>>", self.onSelect);
        self.listbox.bind("<Button-3>", self.popupmenu);
        self.listbox.bind('<Return>', self.openEnter)
        editer.add(self.scrollme);
        self.scrollme.config(command = self.listbox.yview);
        self.totlaitem();

        self.propertylistbox = Listbox(proj, relief=FLAT, width=10);
        self.propertylistbox.insert(0, "Desktop");
        self.propertylistbox.insert(1, "Documents");
        self.propertylistbox.insert(2, "Downloads");
        self.propertylistbox.insert(3, "Music");
        self.propertylistbox.insert(4, "Pictures");
        self.propertylistbox.insert(5, "Videos");
        self.propertylistbox.insert(6, "Windows(C:)");
        self.propertylistbox.insert(7, "Developer(J:)");
        self.propertylistbox.bind("<<ListboxSelect>>", self.onclickside);
        proj.add(self.propertylistbox);


    def totlaitem(self):
        self.fileName = StringVar();
        self.fileNameLabel = Label(self.propertypanel, textvariable=self.fileName, bg="white", fg="gray30", wraplength=195);
        self.fileNameLabel.grid();
        self.fileSize = StringVar();
        self.fileSizeLabel = Label(self.propertypanel, textvariable=self.fileSize, bg="white", fg="gray30");
        self.fileSizeLabel.grid();
        self.fileName.set("Total item: "+str(self.listbox.size()));

    def againfolder(self):
        self.fileName.set("Total item: " + str(self.listbox.size()));
        self.fileSize.set("");
    def entrysearch(self, event):
        self.searchitem.config(bg="white");
        self.searchitem.delete(first=0, last='end');

    def onSelect(self, event):
        try:
            self.copy.config(state=NORMAL);
            self.cut.config(state=NORMAL);
            self.paste.config(state=NORMAL);
            self.itemhide.config(state=NORMAL);
            self.rename.config(state=NORMAL);
            self.delete.config(state=NORMAL);
            self.openbtn.config(state=NORMAL);
            filepropobject = event.widget
            self.filepropertyevent = filepropobject.get(filepropobject.curselection()[0]);
            self.fileproperty = os.stat(os.getcwd()+"\\"+self.filepropertyevent);
            self.fileName.set("Name: "+self.filepropertyevent);
            sizeinkb = floor(self.fileproperty.st_size/1024);
            self.fileSize.set("Size: "+str(floor(self.fileproperty.st_size/1024))+" KB");
            if sizeinkb<=0:
                self.fileSize.set("Size: " + str(self.fileproperty.st_size / 1024) + " Byte");
            elif sizeinkb>1000:
                self.fileSize.set("Size: " + str(floor((self.fileproperty.st_size / 1024)/1024))+"."+ str(floor((((self.fileproperty.st_size / 1024)/1024)-floor((self.fileproperty.st_size / 1024)/1024))*1000))+" MB");
        except IndexError:
            print("");


    def popupmenu(self, eventme):
        self.contextmenu.post(eventme.x_root, eventme.y_root);

    def leftsideeventhandler(self, foldername):
        self.pathvalue.append(os.getcwd());
        os.chdir("C:\\Users\\Aryan Rajput\\"+foldername);
        self.dirpath.delete(first=0, last='end');
        self.dirpath.insert(END, os.getcwd());
        self.contents();

    def onclickside(self, event2):
        try:
            selecteditem =event2.widget
            self.nameitem = selecteditem.get(selecteditem.curselection()[0]);
            if(self.nameitem =='Pictures'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Documents'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Desktop'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Music'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Downloads'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Videos'):
                self.leftsideeventhandler(self.nameitem);
            elif(self.nameitem =='Windows(C:)'):
                self.pathvalue.append(os.getcwd());
                os.chdir("C:\\")
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
                self.contents();
            elif(self.nameitem =='Developer(J:)'):
                self.pathvalue.append(os.getcwd());
                os.chdir("J:\\")
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
                self.contents();
        except IndexError:
            print("");

    def aboutjitendar(self):
        self.abwin = Toplevel(self)
        self.abwin.grid()
        self.abwin.minsize(580, 500);
        self.abwin.maxsize(600, 850);
        self.abwin.title("Jitendar Chauhan");
        self.app = aboutdevloper(self.abwin)

    def contents(self, *args):
        self.buttnhandeler();
        self.listbox.delete(first=0, last='end');
        self.itemno = 0;
        try:
            self.chdirt = str(self.dirpath.get());
            self.item = "";
            self.item = sorted(os.listdir(self.chdirt))
            while (self.itemno < len(self.item)):
                self.listbox.insert(self.itemno, self.item[self.itemno]);
                self.itemno += 1;
            self.againfolder();
        except FileNotFoundError:
            messagebox.showerror("Wrong Directory", "Sorry jitendar Have Entered Wrong Directory Name");



    def buttnhandeler(self):
        self.copy.config(state=DISABLED);
        self.cut.config(state=DISABLED);
        self.paste.config(state=DISABLED);
        self.itemhide.config(state=DISABLED);
        self.rename.config(state=DISABLED);
        self.delete.config(state=DISABLED);
        self.openbtn.config(state=DISABLED);
    def newfile(self):
        open("New file.txt", "w+").close();
        messagebox.showinfo("File Creation", "'New File.txt' has been created.");
        self.contents();
    def newfolder(self):
        os.makedirs("New folder");
        messagebox.showinfo("File Creation", "'New Folder' has been created.");
        self.contents();
    def deletefile(self):
        selectitem = self.listbox.get(self.listbox.curselection()[0])
        try:
            os.remove(selectitem);
            messagebox.showinfo("Delete File", selectitem+" File is Deleted");
        except PermissionError:
            os.rmdir(selectitem);
        self.contents();
    def open(self):
        selectitem = str(self.listbox.get(self.listbox.curselection()[0]));
        try:
            comapre = selectitem.count(".");
            if comapre > 0:
                os.system("start "+selectitem);
            else:
                os.chdir(os.getcwd() + "\\" + selectitem);
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
                self.contents();
        except PermissionError:
            print("");
    def openEnter(self, event):
        eventadd = event.widget;
        newvariable = eventadd.get(eventadd.curselection()[0]);
        try:
            chackvar = str(newvariable);
            comparevar = chackvar.count(".");
            if comparevar > 0:
                os.system("start "+newvariable);
            else:
                os.chdir(os.getcwd()+"\\"+chackvar);
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
                self.contents();

        except EXCEPTION:
            print("");
    def selectalllist(self):
        self.listbox.selection_set(first=0, last='end');

    def rename(self):
        self.renameselectitem = self.listbox.get(self.listbox.curselection()[0]);
        self.renametoplavel = Toplevel(self);
        self.renametoplavel.grid()
        self.renametoplavel.minsize(280, 200);
        self.renametoplavel.maxsize(600, 400);
        self.renametoplavel.title("Rename file");
        self.renametoplavel.configure(bg="lightgray");
        self.app = renamefileclass(self.renametoplavel, self.renameselectitem);
    def chdirback(self):
        try:
            if (len(self.pathvalue) > 0):
                self.forwordvalue.append(self.pathvalue[len(self.pathvalue) - 1]);
                os.chdir(self.pathvalue[len(self.pathvalue) - 1]);
                self.pathvalue.remove(self.pathvalue[len(self.pathvalue) - 1]);
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
            else:
                try:
                    self.forwordvalue.append(os.getcwd())
                    os.chdir("..\\");
                    self.dirpath.delete(first=0, last='end')
                    self.dirpath.insert(END, os.getcwd());
                except EXCEPTION:
                    os.chdir("C:/");
        except EXCEPTION:
            print("Sorry by aryan.")
        self.contents();
    def chdirfor(self):
        try:
            if(len(self.forwordvalue) > 0):
                os.chdir(self.forwordvalue[len(self.forwordvalue)-1]);
                self.forwordvalue.remove(self.forwordvalue[len(self.forwordvalue)-1]);
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
            else:
                self.dirpath.delete(first=0, last='end');
                self.dirpath.insert(END, os.getcwd());
        except EXCEPTION:
            messagebox.showerror("Enough", "I can't go ahead")
        self.contents();

class aboutdevloper:
    def __init__(self, master):
        self.master = master
        self.frame1 = Frame(self.master);
        self.myimage = PhotoImage(file="E:\\PDF Documents\\Python\\MyPhonicsProject\\"+"jitendar.png")
        lab = Label(self.frame1, image=self.myimage, bd=10);
        lab.grid(pady=10, padx=110);
        name = Label(self.frame1, text="Name:   Jitendar Chauhan, Kuldeep Kumar");
        name.grid();
        nickname = Label(self.frame1, text="Nick name:   Aryan Rajput, dag sir(KK)");
        nickname.grid();
        passion = Label(self.frame1, text="Passion:  Programming, Naruto");
        passion.grid();
        intersting = Label(self.frame1, text="Interested:  Robotics, Python, JavaScript, \n PHP, Mysql, Batch Programming, Ruby,\n C, C++, Java, HTML, CSS, \n Prolog, AIML, Lisp, XML. Etc..");
        intersting.grid();
        self.des = Button(self.frame1, text="Close", relief=RIDGE, command=self.destroyabout);
        self.des.grid(pady=30, padx=100)
        self.frame1.grid();

    def destroyabout(self):
        self.master.destroy();

class renamefileclass:
    def __init__(self, master, preName):
        self.prevoiceFileName = preName;
        self.master= master;
        self.emptyfile = PhotoImage(file="file.png");
        lab = Label(self.master, image=self.emptyfile);
        lab.grid(row=1, column=2, padx=20, pady=5)
        titletext1 = Label(self.master, text="Old Name: "+self.prevoiceFileName, wraplength=200);
        titletext1.config(bg="lightgray", fg="black")
        titletext1.grid(row=2, column=2, padx=20);
        lebel = Label(self.master, text="New Rename:");
        lebel.config(bg="lightgray", fg="black")
        lebel.grid(row=3, column=1);
        self.newfilenameentry = Entry(self.master);
        self.newfilenameentry.config(fg="black");
        self.newfilenameentry.grid(row=3, column=2, pady=5);
        cancelbtn = Button(self.master, text="Cancel", command=self.destroyrename);
        cancelbtn.grid(row=4, column=2, pady=16)
        okbtn = Button(self.master, text=" Rename ", command=self.renamereturn);
        okbtn.config(bg="gray", fg="white")
        okbtn.grid(row=4, column=3, pady=16, padx=5);

    def renamereturn(self):
        newnamefile = self.newfilenameentry.get();
        os.renames(self.prevoiceFileName, newnamefile);
        self.destroyrename();
    def destroyrename(self):
        self.master.destroy();

if __name__=="__main__":
    app = AryanFileExplorer(None)
    app.minsize(1000, 700);
    app.configure(bg="lightgray");
    app.title('AryanFileExplorer');
    app.grid()
    app.mainloop()
