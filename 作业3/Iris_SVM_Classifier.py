import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

#加载并预处理数据
iris = datasets.load_iris()
X = iris.data[:, :2]  # 取两个特征
y = iris.target

#划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#训练 SVM 模型
svm_model = SVC(kernel='linear', C=1.0, random_state=42)
svm_model.fit(X_train_scaled, y_train)

#模型评估与输出报告
y_pred = svm_model.predict(X_test_scaled)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=iris.target_names))

#可视化决策边界
plt.figure(figsize=(10, 6))

#生成网格
x_min, x_max = X_test_scaled[:, 0].min() - 0.5, X_test_scaled[:, 0].max() + 0.5
y_min, y_max = X_test_scaled[:, 1].min() - 0.5, X_test_scaled[:, 1].max() + 0.5
XX, YY = np.mgrid[x_min:x_max:200j, y_min:y_max:200j] 

#预测网格中每个点的分类结果
Z_for_predict = np.c_[XX.ravel(), YY.ravel()]
Z_predict = svm_model.predict(Z_for_predict)
Z_predict = Z_predict.reshape(XX.shape) 

plt.pcolormesh(XX, YY, Z_predict, cmap=plt.cm.Paired, alpha=0.5)

#绘制所有的测试样本点
plt.scatter(X_test_scaled[:, 0], X_test_scaled[:, 1], c=y_pred, cmap='coolwarm', edgecolors='k', alpha=0.7)

plt.xlabel("Sepal Length (Standardized)")
plt.ylabel("Sepal Width (Standardized)")
plt.title("SVM Linear Classification on Iris Dataset")

#保存并显示图片
plt.savefig('iris_svm_result.png', dpi=300, bbox_inches='tight')
print("\n图片已保存为: iris_svm_result.png")
plt.show()