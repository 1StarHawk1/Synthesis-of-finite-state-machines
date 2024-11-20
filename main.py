def subordination_rules(regex, markup, A):
    subordination_dependencies = [[] for _ in range(len(regex)+1)]
    for i in range(len(regex)):
        # FIRST RULE
        bracket_counter = 0
        if regex[i] == '(' or regex[i] == '<':
            subordination_dependencies[i+1].append(i)
            for j in range(i, len(regex)):
                if regex[j] == '(' or regex[j] == '<':
                    bracket_counter += 1
                if regex[j] == ')' or regex[j] == '>':
                    if bracket_counter == 1:
                        break
                    else:
                        bracket_counter -= 1
                if regex[j] == '|' and bracket_counter == 1:
                    subordination_dependencies[j+1].append(i)
        #SECOND RULE
        bracket_counter = 0
        if regex[i] == '(' or regex[i] == '<':
            helper = []
            if regex[i] == '<':
                helper.append(i)
            for j in range(i, len(regex)):
                if regex[j] == '(' or regex[j] == '<':
                    bracket_counter += 1
                if regex[j] == ')' or regex[j] == '>':
                    if bracket_counter == 1:
                        subordination_dependencies[j+1] = helper
                        break
                    else:
                        bracket_counter -= 1
                if (regex[j] in A and regex[j+1] not in A) or (regex[j] == '>' and i!=0) and bracket_counter == 1:
                    helper.append(j+1)
        #THIRD RULE
        bracket_counter = 0
        if regex[i] == '>':
            place = i+1
            for j in range (i, -1, -1):

                if regex[j] == '>':
                    bracket_counter += 1
                if regex[j] == '<':
                    if bracket_counter == 1:
                        break
                    else:
                        bracket_counter -= 1
                if (regex[j] in A or regex[j]=='<') and regex[j-1] not in A and bracket_counter == 1:
                    subordination_dependencies[j].append(place)

    for i in range(len(subordination_dependencies)):
        for j in range(len(subordination_dependencies)):
            if i in subordination_dependencies[j]:
                markup[j].extend(x for x in markup[i] if x not in markup[j])
    #print(subordination_dependencies)
    print(markup)
    return markup


def main():
    #regex = '<x|a>a'
    regex = '<x|<b|d>>m<a>(b|d)'
    #regex = '<x><a>'
    #regex = '<x|a>x'
    A = ['x', 'b', 'd', 'm', 'a']
    #A = ['x', 'a']
    markup = [[] for _ in range(len(regex)+1)]
    pre_primary_places = []
    #print(markup)
    counter = 1
    for i in range(len(regex)+1):
        if i == 0:
            markup[i].append(0)
            continue
        if regex[i-1]  in A:
            markup[i].append(counter)
            pre_primary_places.append(i-1)
            counter += 1
    #print(markup)
    markup = subordination_rules(regex, markup, A)
    markup = subordination_rules(regex, markup, A)
    #print(markup)
    #print(pre_primary_places)
    conditions = [[0]]
    i = 0
    table = {a:[] for a in A}
    while i<len(conditions):
        for a in A:
            flag = False
            adding = []
            for c in conditions[i]:

                for p in pre_primary_places:
                    if c in markup[p] and regex[p]==a:
                        adding.extend(markup[p+1])
                        flag = True
                        # if markup[p+1] not in conditions:
                        #     conditions.append(markup[p+1])
            if not flag:
                table[a].append(None)
            else:
                table[a].append(adding)
                if adding not in conditions:
                    conditions.append(adding)
        i+=1
    print(table)
    #print(conditions)
    exit_simbols = markup[-1]
    #print(exit_simbols)
    is_condition_in_regex = []
    for i in range(len(conditions)):
        help = False
        for c in conditions[i]:
            if c in exit_simbols:
                help = True
        if help:
            is_condition_in_regex.append(1)
        else:
            is_condition_in_regex.append(0)
    print(is_condition_in_regex)

    array_table = list(table.values())

    output_matrix = [['   ' for _ in range(len(conditions))] for _ in range(len(conditions))]
    print(table)
    print(array_table)

    keys_list = list(table.keys())
    for key in keys_list:
        # Индексируем элементы в таблице
        for i, element in enumerate(table[key]):
            try:
                # Ищем индекс элемента в conditions
                index = conditions.index(element)
            except ValueError:
                # Если элемент не найден, пропускаем его
                continue
            output_matrix[i][index] = key + '/' + str(is_condition_in_regex[index])


    # Выводим результат
    for row in output_matrix:
        print(row)



if __name__ == '__main__':
    main()


