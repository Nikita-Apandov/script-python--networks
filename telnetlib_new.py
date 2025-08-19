import asyncio # Не работает !!!!!!!!!!
import telnetlib3

async def mikrotik_telnet():
    reader, writer = await telnetlib3.open_connection('192.168.88.1', 23)

    await reader.readuntil('Login: ')
    writer.write('admin\n')

    await reader.readuntil('Password: ')
    writer.write('your_password\n')

    await reader.readuntil('>')
    writer.write('/ip address print\n')

    output = await reader.read(4096)
    print(output)

    writer.write('quit\n')
    writer.close()
    await writer.wait_closed()

asyncio.run(mikrotik_telnet())

