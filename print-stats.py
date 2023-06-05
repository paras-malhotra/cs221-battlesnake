from agents import RandomEnemyAgent, AlphaBetaAgent, QLearningAgent
import train

stats = train.Stats(QLearningAgent())
trainer = train.Trainer([RandomEnemyAgent(1), RandomEnemyAgent(2)])
trainer.train(stats, 10)
stats.printStats()