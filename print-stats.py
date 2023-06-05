from agents import RandomEnemyAgent, AlphaBetaAgent
import train

stats = train.Stats(AlphaBetaAgent(3))
trainer = train.Trainer([RandomEnemyAgent(1), RandomEnemyAgent(2)])
trainer.train(stats, 10)
stats.printStats()