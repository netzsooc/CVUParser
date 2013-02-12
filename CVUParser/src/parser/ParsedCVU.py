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
        
        _sections = self._get_sections(cvu)
        _person = self._personal_data_parsed(_sections)
        _secss = self._non_person_parser(_sections)
        self.cvu = self._merge_data(_person, _secss)

        
    def _merge_data(self, D1, D2):
        d = D1.copy()
        d.update(D2)
        return d
    
    
    def _personal_data_parsed(self, sections):
        if sections == None: return None
        data = sections[1]
        subd = self._get_sections(data, False)
        cvu_id = self._get_by_td(data, 4)
        bplace = self._get_by_td(data, 10)
        name = self._get_name(sections[0])
        bdate = self._get_birth_date(data)
        nationality = self._get_by_td(data, 12)
        gender = self._get_by_td(data, 14)[0]
        address = self._get_by_td(subd[2], 1)
        ids = self._to_dict(subd[3], i = 1)
        phn = self._to_dict(subd[7])
        mail = self._to_dict(subd[5])
        return {"DATOS PERSONALES": {"CVU id": cvu_id, 
                                     "Lugar de nacimiento": bplace, 
                                     "Nombre":name, 
                                     "Fecha de nacimiento": bdate,
                                     "Nacionalidad": nationality,
                                     "Género": gender, "Dirección": address, 
                                     "Identificaciones": ids, "Teléfonos": phn,
                                     "Correos Electrónicos": mail}}
    
    
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
        
        
    def _non_person_parser(self, sub_secs):
        if sub_secs == None: return None
        
        secsy = dict([(el[0].xpath("string()"), el[0].xpath("../../tr/td/table")) 
                      for el in [title.xpath("./tbody/tr/th") 
                                 for title in sub_secs[2:]]])
        jason = {}
            
        for sec in secsy.items():
            temp_dict = {}
        
            for el in sec[1]:
                t = el.xpath("./tbody/tr/td")
                subttle = t[0].xpath("./b")
                cont = t[2].xpath("./table/tbody/tr")
                k = subttle[0].xpath("string()").strip().rstrip().replace("\n", "")
            
                for trel in cont:
                    tmp = []
                    v = " ".join(trel.xpath("string()").split()).strip().rstrip()
                    tmp.append(v)
                    temp_dict[k] = temp_dict.get(k, []) + tmp 
                      
            jason[sec[0]] = temp_dict
                    
        return jason            


octavio = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuOctavio.html")
ebe = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuEbe.html")
karen = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuKaren.html")
hugo = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuHugo.html")
blanca = ParsedCVU("/home/netzsooc/Documents/CVUs/cvuBlanca.html")

active = (octavio, ebe, karen, hugo, blanca)[3]

print(active.cvu["DATOS PERSONALES"]["Fecha de nacimiento"])
for (k,v) in active.cvu.items():
    print(k)
    for (a,b) in v.items():
        print((a, b))

