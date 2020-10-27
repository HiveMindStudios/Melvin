FROM gorialis/discord.py:alpine-master-minimal
WORKDIR /Melvin
COPY . .
RUN pip install youtube-dl asyncio discord.py[voice] requests
ENV token="token"
CMD [ "python", "main.py" ]