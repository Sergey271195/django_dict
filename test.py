import re

string = r':{bc}the amount of space occupied by a three-dimensional object as measured in cubic units (such as quarts or liters) {bc}cubic capacity {dx}see Metric System Table, Weights and Measures Table{/dx}'

def style_filter(value, is_safe = True):
    print(value)
    value = re.sub(r'{bc}', ':', value)
    value = re.sub(r'{ldquo}', '&ldquo;', value)
    value = re.sub(r'{rdquo}', '&rdquo;', value)
    value = re.sub(r'{dx}', '<br/>&#8212; ', value)
    value = re.sub(r'{/dx}', '', value)
    print(value)


style_filter(string)