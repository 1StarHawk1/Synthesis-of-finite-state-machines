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
                if regex[j] in A and regex[j+1] not in A and bracket_counter == 1:
                    helper.append(j+1)
        #THIRD RULE
        bracket_counter = 0
        if regex[i] == '>':
            place = i+1
            for j in range (i, -1, -1):
                if j < 0:
                    break
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

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #regex = '<x|y>y'
    regex = '<x|<b|d>>m<a>(b|d)'
    #regex = 'a<b>(a|c)'
    A = ['x', 'b', 'd', 'm', 'a', 'y', 'c']
    markup = [[] for _ in range(len(regex)+1)]
    print(markup)
    counter = 1
    for i in range(len(regex)+1):
        if i == 0:
            markup[i].append(0)
            continue
        if regex[i-1]  in A:
            markup[i].append(counter)
            counter += 1
    print(markup)
    markup = subordination_rules(regex, markup, A)
    markup = subordination_rules(regex, markup, A)
    #print(markup)



