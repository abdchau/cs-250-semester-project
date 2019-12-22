import tkinter
import tkinter.font as tkFont
import tkinter.ttk as ttk


class Table(ttk.Frame):
	"""use a ttk.TreeView as a multicolumn ListBox"""

	def __init__(self, metadata):
		super(Table, self).__init__(width=100,height=100)
		self.metadata = metadata
		self.tree = None
		self.setup()
		self.tree.bind("<Double-1>", self.OnDoubleClick)

	def setup(self):

		# create a treeview with dual scrollbars
		self.tree = ttk.Treeview(columns=headerList, show="headings")
		vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
		hsb = ttk.Scrollbar(orient="horizontal", command=self.tree.xview)

		self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
		self.tree.grid(column=0, row=0, sticky='nsew', in_=self)

		vsb.grid(column=1, row=0, sticky='ns', in_=self)
		hsb.grid(column=0, row=1, sticky='ew', in_=self)

		# place headings
		for col in headerList:
			self.tree.heading(col, text=col.title())
			self.tree.column(col, width=tkFont.Font().measure(col.title()))

	def buildTree(self, data):
		self.clear()
		for item in data:
			self.tree.insert('', 'end', values=item)

	def clear(self):
		self.tree.delete(*self.tree.get_children())


	def OnDoubleClick(self, event):
		item = self.tree.selection()[0]
		filePath = self.metadata[self.tree.item(item, 'values')[0]][-1]
		with open(filePath, 'r', encoding='utf-8') as f:
			data = f.read()
		
		disp = tkinter.Tk()
		label1 = ttk.Label(disp,wraplength="6i", justify="left", anchor="n", text=data)
		label1.grid()
		disp.mainloop()



headerList = [' docID ','                   Title                     ', '     author      ', '                  url                   ']