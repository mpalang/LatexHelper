test1={'test1': 'Test1'}
test2=' '
test3=test2.encode('unicode-escape')
test4=test2.replace('\u2009','\u0020')
print('A'+test2+'B'+'\n'+'A'+test4+'B')
print(test2==test4)