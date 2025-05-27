# نام فایل: self_adaptive_module.py

import random

import torch
import torch.nn as nn
import torch.optim as optim


class AdaptiveAgent(nn.Module):
    def __init__(self, state_dim, action_dim, hidden_dim=64):
        """
        یک شبکه عصبی ساده جهت تخمین مقدار Q برای هر حالت-عملکرد.

        پارامترها:
          state_dim (int): ابعاد فضای حالت.
          action_dim (int): تعداد عملکردهای ممکن.
          hidden_dim (int): تعداد نورون‌های لایه پنهان.
        """
        super(AdaptiveAgent, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, action_dim),
        )

    def forward(self, state):
        return self.net(state)


class SelfAdaptiveModule:
    def __init__(self, state_dim=10, action_dim=3, lr=0.001):
        """
        ماژول یادگیری تقویتی جهت بهبود خودکار سیستم.

        پارامترها:
          state_dim (int): ابعاد فضای حالت.
          action_dim (int): تعداد عملکردهای ممکن.
          lr (float): نرخ یادگیری.
        """
        self.agent = AdaptiveAgent(state_dim, action_dim)
        self.optimizer = optim.Adam(self.agent.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.memory = []  # حافظه تجربی جهت به‌روزرسانی شبکه
        self.gamma = 0.99  # ضریب تخفیف
        self.action_dim = action_dim

    def remember(self, state, action, reward, next_state, done):
        """
        ذخیره نمونه (state, action, reward, next_state, done) در حافظه.
        """
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state, epsilon=0.1):
        """
        انتخاب عملکرد با استراتژی ε-greedy.
        """
        if random.random() < epsilon:
            return random.randint(0, self.action_dim - 1)
        with torch.no_grad():
            q_values = self.agent(torch.FloatTensor(state))
        return q_values.argmax().item()

    def replay(self, batch_size=16):
        """
        به‌روزرسانی مدل با استفاده از نمونه‌های تصادفی از حافظه.
        """
        if len(self.memory) < batch_size:
            return
        batch = random.sample(self.memory, batch_size)
        loss_total = 0.0
        for state, action, reward, next_state, done in batch:
            state_v = torch.FloatTensor(state)
            next_state_v = torch.FloatTensor(next_state)
            q_values = self.agent(state_v)
            next_q_values = self.agent(next_state_v)
            target = reward + (0 if done else self.gamma * next_q_values.max().item())
            target_v = q_values.clone()
            target_v[action] = target
            loss = self.criterion(q_values, target_v)
            self.optimizer.zero_grad()
            loss.backward()
            self.optimizer.step()
            loss_total += loss.item()
        return loss_total / batch_size
