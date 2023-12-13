from base.director import Director
from base.blocks import Action, Split, Condition, Termination, Save
import asyncio

class Action1(Action):
    async def forward(self, data):
        result = f"{data} Action1 Complete,"
        return result

class Action2(Action):
    async def forward(self, data):
        result = f"{data} Action2 Complete,"#, f"{data} Action2 Complete on try 2,"]
        return result

class Action3(Action):
    async def forward(self, data):
        result = f"{data} Action3 Complete "
        return result

class CustomSplit(Split):
    async def forward(self, data):
        output = [data, data]
        return output

class CustomCondition(Condition):
    async def forward(self, data):
        if len(data) > 70:
            return True
        return False

director = Director(max_concurrent_actions=100, flatten_results = True)
perform_action1 = Action1("Action 1")
perform_action2 = Action2("Action 2")
perform_action2b = CustomSplit("Action 2b")
perform_action3 = Action3("Action 3")
condition_1 = CustomCondition("Condition 1")
save_agent = Save("Example Output", "example_output.txt")
director.subscribe("Initial Call", perform_action1)
director.subscribe("Action 1", perform_action2)
director.subscribe("Action 2", perform_action2b)
director.subscribe("Action 2b", perform_action3)
director.subscribe("Action 2b", condition_1)
director.subscribe("Condition 1", save_agent)


director.run_api(host="0.0.0.0", port=8000)