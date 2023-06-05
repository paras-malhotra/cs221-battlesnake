from agents import RandomEnemyAgent, MinimaxAgent
import train

stats = train.Stats(MinimaxAgent(3))
trainer = train.Trainer([RandomEnemyAgent(1), RandomEnemyAgent(2)])
trainer.train(stats, 10)
stats.printStats()