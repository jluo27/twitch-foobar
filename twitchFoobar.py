import settings;
import socket;

# connection

def connect(s):
    s.connect((settings.HOST,settings.PORT));
    s.send(bytes("PASS " + settings.AUTH + "\r\n","UTF-8"));
    s.send(bytes("NICK " + settings.NICK + "\r\n","UTF-8"));
    s.send(bytes("JOIN #" + settings.JOIN + "\r\n","UTF-8"));

def send(s, message):
    s.send(bytes("PRIVMSG #" + settings.NICK + " :" + message + "\r\n","UTF-8"));
    
def run():
    s = socket.socket();
    connect(s);

    # go through first few lines after connecting
    while True:
        response = str(s.recv(1024));
        if "End of /NAMES list" in response: break; 

    while True:
        response = str(s.recv(1024));
        for line in response.split('\\r\\n'):

            if "PING" in line:
                s.send(line.replace("PING","PONG"));
                continue;
        
            splitLine = line.split(':');
            if len(splitLine)<=2:
                continue;

            user = splitLine[1].split("!")[0];
            msg = ":".join(splitLine[2:len(splitLine)]);
            print(user + ": " + msg);

            if msg == "Foo":
                send(s, user + " Bar");
            
        #if response.startswith("PING"):
        #    s.send(bytes("PONG :tmi.twitch.tv","UTF-8"));
        #else:
            #send(s,"Duck");
            #print(response);
        #sleep(1/settings.RATE);
            
        

if __name__ == "__main__":
    run();
