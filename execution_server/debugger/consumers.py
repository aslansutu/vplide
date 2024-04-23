import json
import os
import asyncio
import subprocess

from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings

class DebuggerConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.debug_name = self.scope["url_route"]["kwargs"]["debug_name"]
        self.debug_group_name = f"debug_{self.debug_name}"
        self.process = None

        await self.channel_layer.group_add(self.debug_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        folder_path = "./media"  
        for file_name in os.listdir(folder_path):
            file_path = os.path.join(folder_path, file_name)
            if file_name != 'output.txt':
                os.remove(file_path)

        await self.channel_layer.group_discard(self.debug_group_name, self.channel_name)

    async def receive(self, text_data):
        if text_data.startswith("{\"files\":"):
            asyncio.create_task(self.once(text_data))
        else:
            await self.command(text_data)
            
    async def command(self, text_data):
        text_data = json.loads(text_data)
        command = text_data['command'].encode()
        self.process.stdin.write(command)
        await self.process.stdin.drain()
        
    async def once(self, text_data):
        text_data = json.loads(text_data)
        filelist = []
        
        for file in text_data["files"]:
            filename = file["name"]
            content = file["content"]
            filepath = os.path.join(settings.MEDIA_ROOT, filename)
            filelist.append(filename)
            
            with open(filepath, "w") as f:
                f.write(content)
            
        if self.debug_name == "python":
            command = ["python3", "-m", "pdb"] + [settings.MEDIA_ROOT + "/" + name for name in filelist]
        elif self.debug_name == "cpp":
            command = ["g++", "-g"] + [settings.MEDIA_ROOT + "/" + name for name in filelist] + ["-o", "output"]
            subprocess.run(command, check=True)
            command = ["gdb", settings.MEDIA_ROOT+"/output"]
        elif self.debug_name == "c":
            command = ["gcc", "-g"] + [settings.MEDIA_ROOT + "/" + name for name in filelist] + ["-o", "output"]
            subprocess.run(command, check=True)
            command = ["gdb", settings.MEDIA_ROOT+"/output"]
        elif self.debug_name == "java":
            command = ["javac", "-g"] + [settings.MEDIA_ROOT + "/" + name for name in filelist] + ["-o", "output"]
            subprocess.run(command, check=True)
            command = ["jdb", settings.MEDIA_ROOT+"/output"]

        self.process = await asyncio.create_subprocess_exec(*command, stdin=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.STDOUT)        

        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
            line = line.decode()
            if settings.MEDIA_ROOT in line:
                line = line.split('/')[-1]
            await self.send(text_data=json.dumps({"message": line.rstrip()}))
            
    async def send_message(self, message):
        await self.channel_layer.group_send(
            self.debug_group_name, {"type": "debug_message", "message": message}
        )

    async def debug_message(self, event):
        message = event["message"]
        await self.send(text_data=json.dumps({"message": message}))
