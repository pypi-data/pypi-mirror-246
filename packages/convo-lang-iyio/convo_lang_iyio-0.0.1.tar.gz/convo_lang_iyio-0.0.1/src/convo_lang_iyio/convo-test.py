
from datetime import datetime
from convoLib import Conversation

def setPinHigh(state):
    print('update state to',state)
    return {
        "success":True,
        "time":str(datetime.now())
    }


convo=Conversation()

convo.callbacks['setPinHigh']=setPinHigh

convo.append(
"""*convo*
> define
__model='gpt-3.5-turbo-1106'
__trackModel=true

# Turn the lights in the user's house on or off
> turnOnOffLights(
    # The state to set the lights to
    state: enum("on" "off")
) -> (

    // setPinHigh would be defined as an extern function written in another language
    return(setPinHigh(eq(state "on")))

    //return({state:state})
)

> system
You are a home automation assistant. please assistant the user to the best or your ability.

> user
It's time for bed, can you turn off the lights

""")

convo.completeAsync()

print('------ convo ------')
print(convo.convo)

print('\n\n\n------ flat ------')
print(convo.messages)
print('\n\n\n------ state ------')
print(convo.state)
print('\n\n\n------ messages ------')
print(convo.syntaxMessages)
