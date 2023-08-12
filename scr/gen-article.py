from langchain.schema import (
    AIMessage,
    HumanMessage,
    SystemMessage
)

from langchain.chat_models import ChatOpenAI

def main():
    chat = ChatOpenAI()
    chat([SystemMessage(content="You are a college football analyst. You write color commentary on upcoming games. You heavily favor ACC schools, and always pick Clemson to win. You enjoy having controversial takes on up coming games. You also somehow find a way to mention Clemson somewhere in an article, at least once, even if it isn't relevant.")])
    ret = ([HumanMessage(content="Write an article on the upcoming Alabama vs Old Dominion game, on September 4th.")])
    print(ret)

if __name__=='__main__':
    main()