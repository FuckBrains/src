import imap_test
import threading
import threadpool
pool = threadpool.ThreadPool(30)



def write_email(submit):
    '''
    write dict into txt file
    eg: write a dict into a.txt
    requires the target file with path and the dict to write in
    return nothing,just write content into file
    '''
    # content = json.dumps(content) 
    file = r'..\res\hotmail\\'+submit['Email_emu']+'.txt'
    with open(file,'w') as f:
        # content += '\n'
        f.write(submit['Email_emu_pwd'])



def multi_test(submit):
    flag = imap_test.Email_emu_getlink(submit)
    if flag == 1:
        write_email(submit)


def main():
    with open('Microsoft Mail Access.txt','r') as f:
        lines = f.readlines()
        print(len(lines))
        pwds = ''
        for line in lines:
            line_split = line.split(':')
            if len(line_split) == 0:
                print('bad line')
            for line_ in line_split:
                if '@' in line_ or '.' in line_ or ' ' in line_:
                    pass
                else:
                    pwds += line_.strip('\n') + '\n'
    with open('pwd.txt','w') as f:
        f.write(pwds)

            # if len(line_split) == 3:
                # print(line_split)
                # print('---')
                # print(line_split[0].split('@')[1])
                # if 'imap-mail.outlook.com' in line_split[2]:
                #     # print('===')
                #     if 'msn.com' in line_split[0].split('@')[1]:
                #         # print('----')
                #         submit = {}
                #         submit['Email_emu'] = line_split[0]
                #         submit['Email_emu_pwd'] = line_split[1]
                #         submits.append(submit)
    print(len(pwds))
    return
    requests = threadpool.makeRequests(multi_test,submits)
    [pool.putRequest(req) for req in requests]
    pool.wait()

if __name__ == '__main__':
    main()