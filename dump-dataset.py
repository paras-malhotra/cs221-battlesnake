from agents import RandomEnemyAgent
import train

agent = train.DataDumpAgent()
trainer = train.Trainer([RandomEnemyAgent(1), RandomEnemyAgent(2)])
trainer.train(agent, 100)
agent.dump('dataset.json')