import requests
import re
import db

def get_alliances(page):
    if page == 1:
        url = 'https://www.affpaying.com/affiliate-networks'
    else:
        url = 'https://www.affpaying.com/affiliate-networks?page=%d'%page        
    s = requests.session()
    res = s.get(url)
    print(res)
    # print(res.text)
    modern_alliance = r"<a class=\"text-blue-dark no-underline hover:text-orange\" href=\"/(.*?)\""
    alliances = re.findall(modern_alliance,res.text)
    # reg_url
    modern_reg_url = r"<a class=\"text-blue-dark border-b border-blue-lighter no-underline\" href=\"(.*?)\""
    reg_urls = re.findall(modern_reg_url,res.text)  
    reg_urls = [url.replace('&amp;','&') for url in reg_urls]  
    # print(alliances)
    # print(reg_urls)
    print('Total %d alliances found in page %d'%(len(alliances),page))
    # print('Total %d urls found in page %d'%(len(reg_urls),page))
    num_ali = len(alliances)
    infos = []
    for i in range(num_ali):
        url = 'https://www.affpaying.com/'+alliances[i]
        info = get_skype_info(s,url)
        # info['alliance'] = alliances[i]
        info['alliance_url'] = reg_urls[i]
        # for item in info:
        #     print(' '*4+item+' : ',info[item])
        infos.append(info)
    s.close()
    return infos

def get_skype_info(s,url):
    infos = {}
    res = s.get(url)
    # alliance_name
    # print('url:',url)
    modern_title = r"<h1 class=\"text-xl\">\n(.*?)\n"
    # print('get_skype_info res.text:',res.text)
    alliance_name = re.findall(modern_title,res.text)[0]
    # print(alliance_name) 
    alliance_name = alliance_name.strip()
    infos['Alliance_name'] = alliance_name.replace('&amp;','&')


    # skype
    modern_key = r'<span class=\"text-grey w-1/3 mr-6 text-xs\">\n(.*?)\n'
    keys = re.findall(modern_key,res.text)
    keys = [key.strip() for key in keys]
    modern_value = r'<span class=\"w-2/3 leading-loose text-xs\">\n(.*?)\n'
    values = re.findall(modern_value,res.text)    
    num_values = len(values)
    for i in range(num_values):
        modern_value_split = r'target=\"_blank\">(.*?)</a>'
        if '</a' in values[i]:
            value = re.findall(modern_value_split,values[i])
            if len(value) == 0:
                modern_value_split = r'rel=\"nofollow\">(.*?)</a>'
                value = re.findall(modern_value_split,values[i])
            value = ','.join(value)
        else:
            value = values[i].strip()
        infos[keys[i]] = value

    # # skype
    modern_skype = r"<span class=\"mr-5 text-grey inline-flex\" data-tippy=\"(.*?)\""
    skypes = re.findall(modern_skype,res.text)
    skypes = ','.join(skypes)
    infos['Skypes'] = skypes

    # # Payment Method
    # modern_payment = r"<a class=\"text-blue hover:text-blue-light\" href=\"/affiliate-networks\?filters=pm:(.*?)\""
    # payment_methods = re.findall(modern_payment,res.text)
    # infos['payment_methods'] = payment_methods


    # # Commission Type
    # modern_commission_type = r"<span class=\"w-2/3 leading-loose text-xs\">\n(.*?)\n"    
    # commission_type = re.findall(modern_commission_type,res.text)
    # infos['commission_type'] = commission_type


    return infos

def test():
    a = '''
        <div class="entity flex justify-between py-3">
        <div class="flex flex-col">
            <div class="flex items-center mb-3">
                <h1 class="text-xl">
                    PrivateCPA
                </h1>
                            </div>
            <div class="flex flex-col mb-3">
                <div class="flex items-center">
    '''
    modern_title = r"<h1 class=\"text-xl\">\n(.*?)\n"
    # print('get_skype_info res.text:',res.text)
    alliance_name = re.findall(modern_title,a)    
    print(alliance_name)
    with open('1.txt','w',encoding='utf-8') as f:
        f.write('1')

def write_infos(infos):
    content = ''
    # content = '|'.join(infos[0].keys())+'\n'
    for info in infos:
        content += '|'.join(info.values())+'\n'
    print(content)
    with open('1.txt','a',encoding='utf-8') as f:
        f.write(content)

def write_head(infos):
    content = '|'.join(infos[0].keys())+'\n'
    # for info in infos:
    #     content += '|'.join(info.values())+'\n'
    with open('1.txt','w') as f:
        f.write(content)

def main():
    for i in range(109):
        if i <69:
            continue
        # if i >3:
        #     break
        infos = get_alliances(i+1)
        db.upload_alliance_info(infos)
        # if i == 0:
        #     write_head(info)
        # write_infos(info)
        

if __name__ == '__main__':
    main()

