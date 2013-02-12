'''
Created on 05/02/2013

@author: netzsooc
'''
from lxml import html
from lxml.html.clean import Cleaner
from cssselect import GenericTranslator


class ParsedCVU(object):
    '''
    classdocs
    '''
    

    def __init__(self, cvu_html_string):
        '''
        Constructor
        '''
        cvu = self.cvu_opener(cvu_html_string)
        
        self._sections = self._get_sections(cvu)
        _sections = self._get_sections(cvu)
        _data = _sections[1]
        _subdata = self._get_sections(_data, False)
        _main_data = _subdata[0]
        _desempeno = _sections[2]
        self.name = self._get_name(_sections[0])
        self.bdate = self._get_birth_date(_data)
        self.id = self._get_by_td(_data, 4)
        self.bplace = self._get_by_td(_data, 10)
        self.nationality = self._get_by_td(_data, 12)
        self.gender = self._get_by_td(_data, 14)[0]
        self.address = self._get_by_td(_subdata[2], 1)
        self.ids = self._to_dict(_subdata[3], i = 1)
        self.phn = self._to_dict(_subdata[7])
        self.mail = self._to_dict(_subdata[5])
        _dsmp = self._get_sections(_sections[2], False)
        self.dsmp = self._to_dict(_dsmp[0])

        
    def _to_dict(self, sub_sec, path = "./tbody", i = 0):
        if sub_sec == None: return None
        element = self._get_sections(sub_sec, 0)[0].xpath(path)[0]
        return dict([(x[0][:-1], x[1]) for x in [[id.xpath("string()").strip().
                                                               replace("\n", "")
                                        for id in ids[i:]] for ids in element]])
        
        
    def cvu_opener(self, cvu_html_string):
        encoding1 = "Windows-1252"
        with open(cvu_html_string, "rU", encoding = encoding1) as f:
            doc = f.read()
        
        doc = doc.replace("Impresión de CVU - CONACyT", "")
        cleaner = Cleaner(style=True, page_structure=False)
        cvu = html.document_fromstring(doc)
        return cleaner.clean_html(cvu)

    
    def _get_name(self, main_sec):
        if main_sec == None: return None
        expr = GenericTranslator().css_to_xpath("tr")
        name = main_sec.xpath(expr)
        out_name = " ".join(name[1].xpath("string()").replace("\n","").split())
        return out_name

  
    def _get_birth_date (self, sub_sec):
        if sub_sec == None: return None
        birth = self._get_by_td(sub_sec, 6)
        if birth == "Not found": return birth
        
        months = """enero febrero marzo abril mayo junio julio agosto 
                    septiembre octubre noviembre diciembre""".split()
        bday = birth.split(" de ")
        bday[1] = str(months.index(bday[1]) + 1)
        bday = "/".join(bday)
        return bday
    
       
    def _get_sections(self, cvu, main_body = True):
        if cvu == None: return None
        expr = GenericTranslator().css_to_xpath("table")
        bodies = cvu.xpath(expr)
        if main_body:
            expr1 = GenericTranslator().css_to_xpath("tr th")
            extra = [bd for bd in bodies if bd.xpath(expr1)]
            extra[0] = bodies[1]
            return extra
        else:
            return bodies[1:]
    
    
    def _get_by_td(self, sub_sec, td):
        if sub_sec == None: return None
        try:
            td_css = GenericTranslator().css_to_xpath("td")
            tds = sub_sec.xpath(td_css)
            return " ".join(tds[td].xpath("string()").replace("\n","").split())
        except:
            return "Not found"             


octavio = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuOctavio.html")
#ebe = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuEbe.html")
#karen = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuKaren.html")
active = octavio


print("CVU id: " + str(active.id))
print("name: " + active.name)
print("bday: " + active.bdate)
print("nation: " + active.nationality)
print("bplace: " + active.bplace)
print("gender: " + active.gender)
print("address: " + active.address)
print("ids: " + str(active.ids))
print("phone: " + str(active.phn))
print("mail: " + str(active.mail))
secsy = dict([(el[0].xpath("string()"), el[0].xpath("../../tr/td/table")) 
              for el in [title.xpath("./tbody/tr/th") 
                         for title in active._sections[2:]]])
jason = {}


for sec in secsy.items():
    temp_dict = {}

    for el in sec[1]:
        t = el.xpath("./tbody/tr/td")
        subttle = t[0].xpath("./b")
        cont = t[2].xpath("./table/tbody/tr")
        k = subttle[0].xpath("string()").strip().replace("\n", "")
    
        for trel in cont:
            tmp = []
            v = trel.xpath("string()").strip().replace("\n", "")
            tmp.append(v)
            temp_dict[k] = temp_dict.get(k, []) + tmp 
              
    jason[sec[0]] = temp_dict
            
print(jason)
