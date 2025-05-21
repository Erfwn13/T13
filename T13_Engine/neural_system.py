import torch
import torch.nn as nn
import torch.optim as optim

class EnhancedNeuralSystem(nn.Module):
    def __init__(self, input_dim, hidden_dims, output_dim, dropout_prob=0.3):
        """
        یک شبکه عصبی چندلایه پیشرفته با استفاده از لایه‌های پنهان متعدد، BatchNorm و Dropout.
        
        پارامترها:
          input_dim (int): تعداد ویژگی‌های ورودی.
          hidden_dims (list[int]): لیست تعداد نورون‌های هر لایه پنهان.
          output_dim (int): تعداد ویژگی‌های خروجی یا کلاس‌های پیش‌بینی.
          dropout_prob (float): احتمال Dropout بین لایه‌ها.
        """
        super(EnhancedNeuralSystem, self).__init__()
        layers = []
        prev_dim = input_dim
        for hidden_dim in hidden_dims:
            layers.append(nn.Linear(prev_dim, hidden_dim))
            layers.append(nn.BatchNorm1d(hidden_dim))
            layers.append(nn.ReLU())
            layers.append(nn.Dropout(dropout_prob))
            prev_dim = hidden_dim
        layers.append(nn.Linear(prev_dim, output_dim))
        self.model = nn.Sequential(*layers)
    
    def forward(self, x):
        return self.model(x)

def train_enhanced_neural_system(model, data_loader, epochs=20, lr=0.001):
    """
    آموزش شبکه عصبی پیشرفته با استفاده از داده‌های نمونه.
    
    از Adam optimizer و scheduler برای کاهش نرخ یادگیری هر چند epoch استفاده می‌کنیم.
    """
    criterion = nn.MSELoss()  # برای مثال یک مسئله رگرسیون
    optimizer = optim.Adam(model.parameters(), lr=lr)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.5)
    
    for epoch in range(epochs):
        model.train()
        epoch_loss = 0.0
        for batch_data, batch_target in data_loader:
            optimizer.zero_grad()
            outputs = model(batch_data)
            loss = criterion(outputs, batch_target)
            loss.backward()
            optimizer.step()
            epoch_loss += loss.item()
        scheduler.step()
        avg_loss = epoch_loss / len(data_loader)
        print(f"Epoch {epoch+1}/{epochs}, Loss: {avg_loss:.4f}")
    
    print("Training complete.")

if __name__ == "__main__":
    # داده‌های نمونه: 200 نمونه با 20 ویژگی ورودی و هدف 10 بعدی
    dummy_data = torch.randn(200, 20)
    dummy_target = torch.randn(200, 10)
    
    dataset = torch.utils.data.TensorDataset(dummy_data, dummy_target)
    data_loader = torch.utils.data.DataLoader(dataset, batch_size=16, shuffle=True)
    
    # تعریف مدل پیشرفته؛ در اینجا دو لایه پنهان با 64 و 32 نورون استفاده شده است.
    model = EnhancedNeuralSystem(input_dim=20, hidden_dims=[64, 32], output_dim=10, dropout_prob=0.3)
    train_enhanced_neural_system(model, data_loader, epochs=20, lr=0.001)