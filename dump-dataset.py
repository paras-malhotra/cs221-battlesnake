from agents import RandomAgent
import train

agent = train.DataDumpAgent()
trainer = train.Trainer([RandomAgent(), RandomAgent()])
trainer.train(agent, 100)
agent.dump('dataset.json')