from HTMLTable import HTMLTable
def fix_the_list(the_list):
    '''
    使得the_list每一行都有相同数量的元素，这个数量是the_list行中数量的最大值。
    达不到最大值值的行，在行末用空字符填充
    '''
    try:
        max_len=max(len(row) for row in the_list)
    except:
        max_len=0
    for i in range(len(the_list)):
        row_len=len(the_list[i])
        if row_len<max_len:
            for j in range(max_len-row_len):
                the_list[i].append("")

def convert_list_to_html(the_list,title):
    if type(the_list)!=list:
        raise TypeError("参数错误，the_list必须是列表")
    for row in the_list:
        if type(row)!=list:
            raise TypeError("参数错误,the_list内所有元素必须都为列表")
    fix_the_list(the_list)
    table=HTMLTable(caption=title)
    table.append_data_rows(the_list)
    table.caption.set_style({
    'font-size': '20px',
    })
    table.set_style({
    'border-collapse': 'collapse',
    'word-break':'break-all',
    'word-wrap':'break-word',
    #'white-space': 'nowrap',
    'width':"400px",
    'font-size': '14px',
    })
    table.set_cell_style({
    'border-color': '#000',
    'border-width': '1px',
    'word-break':'break-all',
    'word-wrap': 'break-word',
    'border-style': 'solid',
    'padding': '5px',
    'width':"400px",
    })
    return table.to_html()

class ldl_html_class:
    def __init__(self) -> None:
        self.html=""
    def add_text(self,size,text,**argvs):
        stylestr="\"font-size:"+str(size)+"px;"
        for key in argvs:
            tempkey=str(key).replace("_","-")+":"+str(argvs[key])+";"
            stylestr+=tempkey
        stylestr+="\">"

        temp="<p style="+stylestr+text+"</p>"
        self.html+=temp
    def add_table(self,the_list,title):
        temp=convert_list_to_html(the_list,title)
        self.html+=temp
    def to_str(self):
        return self.html
