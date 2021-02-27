for messages_count in range(0, 100):
    remainder = messages_count % 10
    if messages_count == 0:
        print('У вас нет новых сообщений')
    elif remainder == 0 or remainder>=5 or 11 >= messages_count <= 19:
        print('У вас', messages_count, 'новых сообщений')
    elif remainder == 1 and messages_count != 11:
        print('У вас', messages_count , 'новое сообщение')
    else:
        print('У вас', messages_count, 'новых сообщения')
