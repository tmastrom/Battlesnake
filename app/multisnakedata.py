#127.0.0.1 - - [22/Feb/2019 18:50:06] "POST /start HTTP/1.1" 200 20

# for quick testing 


data = {
    "turn": 0, 
    "game": 
        {"id": "fd220166-f16b-447f-97ea-5d40ac41180c"}, 
    "board": 
        {"food": 
            [{"y": 3, "x": 1}, {"y": 3, "x": 2}, 
            {"y": 0, "x": 0}, {"y": 2, "x": 2}, 
            {"y": 4, "x": 1}, {"y": 1, "x": 2}, 
            {"y": 2, "x": 4}, {"y": 2, "x": 3}, 
            {"y": 0, "x": 2}, {"y": 4, "x": 2}],
        "width": 5, 
        "snakes": 
            [{"body": 
                [{"y": 3, "x": 4}, {"y": 3, "x": 4}, {"y": 3, "x": 4}], 
                "health": 100, 
                "id": "89ad4e11-d77d-45c5-bd83-4f660f1752af", 
                "name": "me "}, 
            {"body": 
                [{"y": 4, "x": 3}, {"y": 4, "x": 3}, 
                {"y": 4, "x": 3}], 
                "health": 100, 
                "id": "c95a0e29-7c57-4cd7-92e2-66925e675b3f", 
                "name": "tommy-yum"}, 
            {"body": 
                [{"y": 4, "x": 0}, {"y": 4, "x": 0}, {"y": 4, "x": 0}], 
                "health": 100, 
                "id": "9dc58c94-90d6-45f5-b94c-10da47a02d9d", 
                "name": "sem"}], 
                "height": 5}, 
        "you": 
            {"body": 
                [{"y": 3, "x": 4}, {"y": 3, "x": 4}, {"y": 3, "x": 4}], 
                "health": 100, 
                "id": "89ad4e11-d77d-45c5-bd83-4f660f1752af", 
                "name": "me "}}

dont = []
'''for i in data["board"]["snakes"]:
    for j in i['body']:
        pos = [j['x'],j['y']]
        dont.append(pos)
#print dont, 'DONT'
'''
for i in data["board"]["snakes"]:
    pos = [i['body'][0]['x'],i['body'][0]['y']]
    dont.append(pos) 
#print dont
x = data['board']['width']
#print x

head = [int(data["you"]["body"][0]["x"]), int(data["you"]["body"][0]["y"])]

threeby = [[head[0], head[1]-1],
[head[0], head[1]+1],
[head[0]-1, head[1]],
[head[0]-1, head[1]-1],
[head[0]-1, head[1]+1],
[head[0]+1, head[1]],
[head[0]+1, head[1]-1],
[head[0]+1, head[1]+1]]

print threeby

print data["you"]["body"][1]